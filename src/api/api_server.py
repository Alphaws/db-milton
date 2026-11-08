import http.server
import json
import os
import re
import subprocess
import time
from collections import defaultdict

PORT = 8000
DB_HOST = os.environ.get("DB_HOST", "mariadb")
DB_USER = os.environ.get("DB_USER", "webshop_user")
DB_PASS = os.environ.get("DB_PASSWORD", "webshop_password")
DB_NAME = os.environ.get("DB_NAME", "webshop_eav_db")

# In-memory Rate Limiter IP címekre (DoW / DoS védelem)
# IP -> list of timestamps
IP_REQUESTS = defaultdict(list)
RESET_REQUESTS = defaultdict(list)
RATE_LIMIT_QUERIES = 20  # max 20 lekérdezés / 10 mp / IP
RATE_LIMIT_RESETS = 2    # max 2 reset / 30 mp / IP

# Tiltott, destruktív / privilege escalation parancsok, amik tönkretehetik a konténert vagy a szervert
FORBIDDEN_PATTERNS = [
    r"\bDROP\s+DATABASE\b",
    r"\bCREATE\s+DATABASE\b",
    r"\bALTER\s+DATABASE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bFLUSH\b",
    r"\bINTO\s+OUTFILE\b",
    r"\bINTO\s+DUMPFILE\b",
    r"\bLOAD_FILE\b",
    r"\bLOAD\s+DATA\b",
    r"\bSHUTDOWN\b",
    r"\bSYSTEM\b",
    r"\bEXEC\b",
    r"\\\!" # MariaDB shell escape
]

def is_rate_limited(ip, is_reset=False):
    now = time.time()
    history = RESET_REQUESTS[ip] if is_reset else IP_REQUESTS[ip]
    window = 30 if is_reset else 10
    limit = RATE_LIMIT_RESETS if is_reset else RATE_LIMIT_QUERIES
    
    # Régi timestamp-ek törlése
    history[:] = [t for t in history if now - t < window]
    if len(history) >= limit:
        return True
    history.append(now)
    return False

def check_sql_safety(sql):
    upper = sql.upper()
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, upper):
            return False, f"Biztonsági korlátozás: A '{pat}' jellegű adminisztratív vagy fájlművelet tiltott a publikus sandboxban!"
    
    # Maximum query hossz (pl. 4000 karakter) puffer túlcsordulás vagy memóriatúlterhelés ellen
    if len(sql) > 4000:
        return False, "A lekérdezés hossza meghaladja a megengedett 4000 karakteres határt!"
        
    return True, None

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def get_client_ip(self):
        # Ha Nginx / Traefik mögött vagyunk
        forwarded = self.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        real_ip = self.headers.get('X-Real-IP')
        if real_ip:
            return real_ip.strip()
        return self.client_address[0]

    def do_POST(self):
        client_ip = self.get_client_ip()

        if self.path == '/api/reset':
            if is_rate_limited(client_ip, is_reset=True):
                self._send_json({"error": "Túl sok reset kérés! Kérlek várj pár másodpercet az újabb visszaállítás előtt."}, 429)
                return

            sql_file_path = "/app/webshop_eav_modell.sql"
            if not os.path.exists(sql_file_path):
                sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "sql", "webshop_eav_modell.sql")

            try:
                with open(sql_file_path, "r", encoding="utf-8") as f:
                    sql_content = f.read()

                cmd = [
                    "mariadb",
                    f"-h{DB_HOST}",
                    f"-u{DB_USER}",
                    f"-p{DB_PASS}"
                ]
                res = subprocess.run(cmd, input=sql_content, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
                if res.returncode != 0:
                    self._send_json({"error": "Reset hiba: " + res.stderr.strip()}, 500)
                else:
                    self._send_json({"message": "Az adatbázis sikeresen visszaállítva az eredeti állapotra (7 tábla, példaadatok újratöltve)!"})
            except subprocess.TimeoutExpired:
                self._send_json({"error": "A reset művelet túllépte az időkorlátot!"}, 408)
            except Exception as e:
                self._send_json({"error": "Reset kivétel: " + str(e)}, 500)
            return

        if self.path == '/api/execute':
            if is_rate_limited(client_ip, is_reset=False):
                self._send_json({"error": "Túl sok kérés erről az IP címről! Kérlek várj pár másodpercet."}, 429)
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                body = json.loads(post_data)
                sql_query = body.get('sql', '').strip()
                if not sql_query:
                    self._send_json({"error": "Üres SQL lekérdezés!"}, 400)
                    return

                # Biztonsági elemzés (fájlműveletek, drop database, shell escape tiltása)
                safe, err_msg = check_sql_safety(sql_query)
                if not safe:
                    self._send_json({"error": err_msg}, 403)
                    return

                # Futtatás szigorú izolációban és 6 másodperces időkorláttal (ReDoS / infinite lock ellen)
                cmd = [
                    "mariadb",
                    f"-h{DB_HOST}",
                    f"-u{DB_USER}",
                    f"-p{DB_PASS}",
                    DB_NAME,
                    "-e", sql_query
                ]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=6)
                
                if res.returncode != 0:
                    self._send_json({"error": res.stderr.strip()}, 400)
                    return

                output_lines = res.stdout.strip().split("\n")
                if not output_lines or output_lines == ['']:
                    self._send_json({"columns": [], "rows": [], "affected": "Sikeres parancsfuttatás (DML: INSERT / UPDATE / DELETE / DDL végrehajtva)."})
                    return

                columns = output_lines[0].split("\t")
                rows = []
                for line in output_lines[1:]:
                    if line:
                        rows.append(line.split("\t"))

                self._send_json({"columns": columns, "rows": rows, "count": len(rows)})

            except subprocess.TimeoutExpired:
                self._send_json({"error": "A lekérdezés futási ideje túllépte a megengedett 6 másodperces korlátot!"}, 408)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    print(f"Biztonságos SQL Sandbox API elindult a(z) {PORT} porton...")
    server = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), RequestHandler)
    server.serve_forever()
