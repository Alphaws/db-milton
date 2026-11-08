import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 képarány beállítása (13.333 x 7.5 hüvelyk)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Színpaletta
    C_BG = RGBColor(11, 15, 25)
    C_CARD = RGBColor(19, 28, 48)
    C_CARD_BORDER = RGBColor(38, 52, 84)
    C_TEXT = RGBColor(243, 244, 246)
    C_MUTED = RGBColor(160, 170, 185)
    C_TEAL = RGBColor(45, 212, 191)
    C_INDIGO = RGBColor(99, 102, 241)
    C_AMBER = RGBColor(245, 158, 11)
    C_ROSE = RGBColor(244, 63, 94)

    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, lead_text=""):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = tag_text.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL
        p.font.name = "Calibri"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT
        p2.font.name = "Calibri"

        if lead_text:
            lead_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.45))
            tf3 = lead_box.text_frame
            tf3.word_wrap = True
            tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
            p3 = tf3.paragraphs[0]
            p3.text = lead_text
            p3.font.size = Pt(12)
            p3.font.color.rgb = C_MUTED
            p3.font.name = "Calibri"

    def add_card(slide, left, top, width, height, title, body_paragraphs, border_color=C_CARD_BORDER, font_size=10.5):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.22)

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = C_TEXT
            p.font.name = "Calibri"
            p.space_after = Pt(4)
            first_body = True
        else:
            first_body = False

        for item in body_paragraphs:
            if not title and not first_body:
                p = tf.paragraphs[0]
                first_body = True
            else:
                p = tf.add_paragraph()
            p.text = item
            p.font.size = Pt(font_size)
            p.font.color.rgb = C_MUTED
            p.font.name = "Calibri"
            p.space_after = Pt(2)

        return card

    # ==========================================
    # DIA 1: CÍMLAP
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    # Milton Friedman Egyetem hivatalos logó elhelyezése
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "milton_logo_feher.png")
    s1.shapes.add_picture(logo_path, Inches(1.0), Inches(0.55), Inches(3.2), Inches(0.9))

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(3.2))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "MILTON FRIEDMAN EGYETEM · BH-MIT059-L: ADATBÁZISKEZELÉS 2."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Korszerű Webshop Adatmodell\nEntity-Attribute-Value (EAV) Architektúrában"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT
    p2.space_after = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "Heterogén e-kereskedelmi termékkatalógus és tranzakciós rendelési alrendszer tervezése relációs adatbázisban a 3. normálforma (3NF) szigorú megtartásával."
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_MUTED
    p3.space_after = Pt(12)

    p4 = tf1.add_paragraph()
    p4.text = "Készítette: Szeness Imre   |   Neptun: TQJH7P   |   Oktató: Szabó István Gábor   |   Félév: 2026/27/1"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = C_AMBER

    add_card(s1, 1.0, 5.2, 3.5, 1.6, "Adatbázis", ["MariaDB 11.4 / MySQL", "7 Normalizált Reláció", "Karakterkészlet: utf8mb4"], C_INDIGO, 11)
    add_card(s1, 4.9, 5.2, 3.5, 1.6, "Kulcskövetelmények", ["Két összetett PK tábla", "EAV Pivot lekérdezések", "10+ példasor minden táblában"], C_TEAL, 11)
    add_card(s1, 8.8, 5.2, 3.5, 1.6, "Környezet", ["100% Dockerizált", "Adminer GUI webes felület", "Automata inicializálás"], C_AMBER, 11)

    # ==========================================
    # DIA 2: SZKÓP ÉS PROBLÉMA
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "01. Dia · Probléma és Megoldás", "Miért szükséges az EAV Modell az E-kereskedelemben?", 
               "Valós életből vett kihívás a különböző műszaki paraméterekkel bíró heterogén termékek tárolásánál.")

    add_card(s2, 0.8, 2.05, 5.7, 4.9, "A Hagyományos Modell Korlátai", [
        "Egy modern webáruházban egymás mellett találhatók laptopok (RAM, CPU), cipők (EU méret, talptípus) és kávéfőzők (teljesítmény, nyomás).",
        "",
        "❌ Hagyományos megközelítés (Ritka tábla):",
        "• Egyetlen products tábla 150+ oszloppal.",
        "• Az adatrekordok mezőinek 90%-a feleslegesen NULL.",
        "• Új kategória esetén ALTER TABLE sémamódosítás kell az éles adatbázison, ami kockázatos és leállással járhat.",
        "",
        "❌ Kategóriánkénti külön táblák:",
        "• Táblarobbanás (pl. 50 külön terméktábla).",
        "• Közös lekérdezések és globális kosárkezelés rendkívül nehézkes megvalósítása."
    ], C_ROSE, 11)

    add_card(s2, 6.8, 2.05, 5.7, 4.9, "A Választott Megoldás: EAV Modell", [
        "Az Entity-Attribute-Value minta a tulajdonságokat sorként kezeli az oszlopok bővítése helyett, teljes 3NF normalizálás mellett.",
        "",
        "✅ 1. Entity (Entitás) – 'products':",
        "Csak a globális, minden cikkre érvényes törzsadatok (cikkszám, név, alap eladási ár, raktárkészlet, státusz).",
        "",
        "✅ 2. Attribute (Attribútum) – 'attributes':",
        "A dinamikus tulajdonságok jegyzéke (kód, név, adattípus, mértékegység).",
        "",
        "✅ 3. Value (Érték) – 'product_attribute_values':",
        "Összetett elsődleges kulcsos (product_id, attribute_id) kapcsolótábla típusbiztos oszlopokkal (varchar, number, datetime)."
    ], C_TEAL, 11)

    # ==========================================
    # DIA 3: BACHMAN ÁBRA
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "02. Dia · Kapcsolati Terv", "Bachman / ER Relációs Diagram", 
               "A 7 normalizált reláció mezőszintű Bachman ábrája 1:N irányított kapcsolatokkal és összetett kulcsokkal.")

    # A professzionális nagyfelbontású Bachman ábra beágyazása
    bachman_img_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "bachman_diagram.png")
    s3.shapes.add_picture(bachman_img_path, Inches(0.8), Inches(2.0), Inches(11.73), Inches(5.1))

    # ==========================================
    # DIA 4: TÁBLÁK - EAV SPECIFIKÁCIÓ (OPTIMALIZÁLT MÉRETEZÉS ÉS BETŰMÉRET)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "03. Dia · Adatbázis Táblák 1.", "Katalógus és EAV Táblák Specifikációja", 
               "Legalább 3 mező, típusbiztos oszlopok és szigorú idegen kulcs kényszerek.")

    add_card(s4, 0.8, 2.05, 3.7, 5.0, "1. categories & products", [
        "categories (Hierarchikus):",
        "• category_id (PK, AUTO_INCREMENT)",
        "• parent_id (FK -> categories, NULL)",
        "• name, slug (UNIQUE NOT NULL)",
        "• created_at (DATETIME)",
        "",
        "products (Mag Entitás):",
        "• product_id (PK, AUTO_INCREMENT)",
        "• category_id (FK -> categories)",
        "• sku (VARCHAR 50, UNIQUE)",
        "• name (VARCHAR 255)",
        "• base_price (DECIMAL 12,2)",
        "• stock_qty (INT DEFAULT 0)",
        "• is_active (TINYINT 1)",
        "• created_at (DATETIME)"
    ], C_INDIGO, 9.5)

    add_card(s4, 4.8, 2.05, 3.7, 5.0, "2. attributes Metaadatok", [
        "attributes (Attribútumok):",
        "Dinamikus tulajdonságok jegyzéke:",
        "",
        "• attribute_id (PK, AUTO_INCREMENT)",
        "• code (VARCHAR 50, UNIQUE)",
        "  pl. 'color', 'ram_size', 'weight_kg'",
        "• name (VARCHAR 100) - megnevezés",
        "• data_type (ENUM):",
        "  varchar, int, decimal, datetime, boolean",
        "• unit (VARCHAR 20) - pl. GB, kg, EU",
        "• description (VARCHAR 255)",
        "",
        "Kódmódosítás nélkül, admin felületről",
        "bővíthető paraméter-katalógus."
    ], C_TEAL, 9.5)

    add_card(s4, 8.8, 2.05, 3.7, 5.0, "3. product_attribute_values", [
        "product_attribute_values (Értékek):",
        "Összetett Kulcsos Kapcsolótábla:",
        "",
        "• product_id (PK, FK -> products)",
        "• attribute_id (PK, FK -> attributes)",
        "",
        "Típushelyes tárolómezők:",
        "• value_varchar (VARCHAR 255)",
        "  pl. 'Titán natúr', 'Bőr / textil'",
        "• value_number (DECIMAL 12,4)",
        "  pl. 128 (GB), 6.1 (col), 43.5",
        "• value_datetime (DATETIME)",
        "• created_at (DATETIME)",
        "",
        "PK(product_id, attribute_id) garantálja",
        "a pontosan 1 érték integritást."
    ], C_AMBER, 9.5)

    # ==========================================
    # DIA 5: TÁBLÁK - RENDELÉSI ALRENDSZER
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "04. Dia · Adatbázis Táblák 2.", "Vásárlók és Megrendelések Alrendszere", 
               "Tranzakciókezelés, összetett kulcsos tételsorok és származtatott kalkulációk.")

    add_card(s5, 0.8, 2.05, 3.7, 5.0, "4. customers Tábla", [
        "Vásárlói törzsadatok:",
        "",
        "• customer_id (PK, AUTO_INCREMENT)",
        "• first_name (VARCHAR 50)",
        "• last_name (VARCHAR 50)",
        "• email (VARCHAR 150, UNIQUE NOT NULL)",
        "• phone (VARCHAR 30)",
        "• registration_date (DATETIME NOT NULL)",
        "",
        "Kapcsolat az orders felé: 1 : N.",
        "Minden vevőhöz több rendelés kapcsolódhat."
    ], C_CARD_BORDER, 10.5)

    add_card(s5, 4.8, 2.05, 3.7, 5.0, "5. orders Tábla", [
        "Megrendelés Fejléc:",
        "",
        "• order_id (PK, AUTO_INCREMENT)",
        "• customer_id (FK -> customers)",
        "• order_date (DATETIME NOT NULL)",
        "• total_amount (DECIMAL 12,2)",
        "• status (ENUM):",
        "  'pending', 'paid', 'shipped', 'cancelled'",
        "• shipping_address (VARCHAR 255)",
        "• payment_method (VARCHAR 50)",
        "",
        "Központi tranzakciós tábla állapotkövetéssel."
    ], C_ROSE, 10.5)

    add_card(s5, 8.8, 2.05, 3.7, 5.0, "6. order_items Tábla", [
        "Rendelés Tételek (Összetett Kulcs):",
        "",
        "• order_id (PK, FK -> orders, CASCADE)",
        "• product_id (PK, FK -> products, RESTRICT)",
        "• quantity (INT NOT NULL DEFAULT 1)",
        "• unit_price (DECIMAL 12,2 NOT NULL)",
        "",
        "Származtatott generált mező:",
        "• subtotal (DECIMAL 12,2)",
        "  GENERATED ALWAYS AS (quantity * unit_price)",
        "",
        "PK(order_id, product_id) biztosítja a 3NF-et."
    ], C_AMBER, 10.5)

    # ==========================================
    # DIA 6: SQL 1 ÉS 2 LEKÉRDEZÉSEK
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "05. Dia · SQL Használat 1.", "Kötelező Lekérdezések: Egytáblás és Függvényes", 
               "A feladatkiírás 1. és 2. típusú lekérdezési mintája MariaDB / MySQL szintaxissal.")

    add_card(s6, 0.8, 2.05, 5.7, 4.9, "1. Egyszerű Egytáblás Szűrés és Rendezés", [
        "SELECT product_id, sku, name, base_price, stock_qty",
        "FROM products",
        "WHERE is_active = 1",
        "ORDER BY base_price DESC;",
        "",
        "Magyarázat:",
        "• Csak az aktív (értékesíthető) termékek lekérdezése.",
        "• Csökkenő ár szerinti rendezés (a prémium laptopoktól az olcsóbb kiegészítők felé).",
        "",
        "Eredmény: 10 aktív rekord rendezett listája."
    ], C_CARD_BORDER, 11)

    add_card(s6, 6.8, 2.05, 5.7, 4.9, "2. Aggregáló Függvények és Csoportosítás", [
        "SELECT ",
        "    c.name AS kategoria_nev,",
        "    COUNT(p.product_id) AS termek_db,",
        "    MIN(p.base_price) AS legolcsobb_ar_huf,",
        "    MAX(p.base_price) AS legdragabb_ar_huf,",
        "    ROUND(AVG(p.base_price), 2) AS atlagos_ar_huf",
        "FROM categories c",
        "LEFT JOIN products p ON c.category_id = p.category_id",
        "GROUP BY c.category_id, c.name",
        "HAVING termek_db > 0",
        "ORDER BY atlagos_ar_huf DESC;",
        "",
        "Alkalmazott függvények: COUNT, MIN, MAX, AVG, ROUND + HAVING feltétel."
    ], C_TEAL, 10.5)

    # ==========================================
    # DIA 7: SQL 3 ÉS 4 LEKÉRDEZÉSEK
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "06. Dia · SQL Használat 2.", "Kötelező Lekérdezések: EAV Pivot JOIN és Allekérdezés", 
               "A feladatkiírás 3. és 4. típusú lekérdezési mintája.")

    add_card(s7, 0.8, 2.05, 5.7, 4.9, "3. Összetett Többtáblás Lekérdezés EAV Pivottal", [
        "SELECT ",
        "    o.order_id, o.order_date,",
        "    CONCAT(c.last_name, ' ', c.first_name) AS vasarlo,",
        "    p.name AS termek, oi.quantity AS db, oi.subtotal,",
        "    COALESCE(pav_color.value_varchar, '-') AS szin,",
        "    CONCAT(COALESCE(pav_storage.value_number, 0), ' GB') AS tarhely",
        "FROM orders o",
        "JOIN customers c ON o.customer_id = c.customer_id",
        "JOIN order_items oi ON o.order_id = oi.order_id",
        "JOIN products p ON oi.product_id = p.product_id",
        "LEFT JOIN product_attribute_values pav_color ",
        "    ON p.product_id = pav_color.product_id AND pav_color.attribute_id = 1",
        "LEFT JOIN product_attribute_values pav_storage ",
        "    ON p.product_id = pav_storage.product_id AND pav_storage.attribute_id = 2",
        "WHERE o.status IN ('paid', 'shipped');",
        "",
        "EAV értékek oszlopokká pivotolása relációs JOIN segítségével."
    ], C_AMBER, 10)

    add_card(s7, 6.8, 2.05, 5.7, 4.9, "4. Allekérdezést (Subquery) Tartalmazó Lekérdezés", [
        "SELECT ",
        "    c.customer_id,",
        "    CONCAT(c.last_name, ' ', c.first_name) AS vasarlo,",
        "    COUNT(o.order_id) AS rendelesek_szama,",
        "    SUM(o.total_amount) AS ossz_koltes",
        "FROM customers c",
        "JOIN orders o ON c.customer_id = o.customer_id",
        "WHERE o.status <> 'cancelled'",
        "GROUP BY c.customer_id, c.last_name, c.first_name",
        "HAVING SUM(o.total_amount) > (",
        "    -- Belső Allekérdezés: rendelések átlagos értéke",
        "    SELECT AVG(total_amount) ",
        "    FROM orders WHERE status <> 'cancelled'",
        ")",
        "ORDER BY ossz_koltes DESC;",
        "",
        "Azon kiemelt vevők szűrése, akik az átlag felett költöttek."
    ], C_INDIGO, 10.5)

    # ==========================================
    # DIA 8: DOCKER ÉS KÖRNYEZET
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "07. Dia · Konténerizáció", "Docker Környezet és Üzemeltetés", 
               "Azonnal indítható, hordozható és reprodukálható mikroarchitektúra.")

    add_card(s8, 0.8, 2.05, 3.7, 3.5, "MariaDB 11.4 Konténer", [
        "• Port: 3306",
        "• Felhasználó: webshop_user",
        "• Adatbázis: webshop_eav_db",
        "• Automatikus DDL és DML inicializálás a webshop_eav_modell.sql fájlból."
    ], C_TEAL, 11)

    add_card(s8, 4.8, 2.05, 3.7, 3.5, "Adminer Webes GUI", [
        "• Cím: http://localhost:8085",
        "• Grafikus adatbáziskezelő",
        "• Támogatja az SQL parancsok futtatását és a táblák böngészését."
    ], C_INDIGO, 11)

    add_card(s8, 8.8, 2.05, 3.7, 3.5, "Nginx Web Prezentáció", [
        "• Cím: http://localhost:8086",
        "• Interaktív HTML/CSS/JS diavetítő rendszer.",
        "• Billentyűzetvezérlés és kódmásolás."
    ], C_AMBER, 11)

    add_card(s8, 0.8, 5.85, 11.7, 1.1, "Indítási Parancs:", [
        "docker compose up -d (A beadando3 mappában futtatva mindhárom szolgáltatás azonnal elindul)"
    ], C_CARD_BORDER, 11)

    # ==========================================
    # DIA 9: KÖVETELMÉNYEK ELLENŐRZŐJE
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "08. Dia · Összegzés", "Tantárgyi Követelmények Ellenőrzése", 
               "Minden előírt tervezési feltétel tételes verifikációja.")

    add_card(s9, 0.8, 2.05, 5.7, 4.9, "Strukturális Követelmények", [
        "✓ Legalább 5-6 tábla:",
        "  Megvalósítva: 7 normalizált reláció.",
        "",
        "✓ Legalább 3. normálforma (3NF):",
        "  Minden nem-kulcs mező közvetlenül a teljes kulcstól függ (nincs részleges vagy tranzitív függőség).",
        "",
        "✓ Legalább 3 mező táblánként:",
        "  Minden táblában 5-8 értelmes adatmező található.",
        "",
        "✓ Legalább egy összetett elsődleges kulcs:",
        "  Két táblában is: product_attribute_values és order_items.",
        "",
        "✓ Legalább egy dátum mező:",
        "  created_at, registration_date, order_date mezők."
    ], C_TEAL, 11)

    add_card(s9, 6.8, 2.05, 5.7, 4.9, "Adat és Lekérdezési Követelmények", [
        "✓ PK - FK relációs integritás:",
        "  Szigorú idegen kulcsok ON DELETE CASCADE és RESTRICT szabályokkal.",
        "",
        "✓ Legalább 10 sornyi példaadat táblánként:",
        "  Mind a 7 tábla 10-15 életszerű rekorddal inicializálva.",
        "",
        "✓ 4 Kötelező Lekérdezési Típus:",
        "  1. Egyszerű egytáblás (aktív termékek csökkenő árban)",
        "  2. Függvényhasználatos (COUNT, MIN, MAX, AVG, ROUND, HAVING)",
        "  3. Összetett többtáblás EAV pivottal",
        "  4. Allekérdezés (HAVING SUM > (SELECT AVG))",
        "",
        "✓ Dockerizált kivitelezés: MariaDB 11.4 + Adminer + Nginx"
    ], C_AMBER, 11)

    output_path = os.path.join(os.path.dirname(__file__), "..", "docs", "Webshop_EAV_Adatbazistervezes_Prezentacio.pptx")
    prs.save(output_path)
    print(f"Sikeres mentés: {output_path}")

if __name__ == "__main__":
    create_deck()
