# Webshop EAV Adatbázis Modell és Interaktív Prezentációs Környezet

**Intézmény:** Milton Friedman Egyetem  
**Kurzus:** BH-MIT059-L: Adatbáziskezelés 2.  
**Oktató:** Szabó István Gábor  
**Hallgató:** Szeness Imre  
**Neptun kód:** TQJH7P  
**Félév:** 2026/27/1  

---

## 🌐 Publikus Elérhetőségek

- 🚀 **Élő Webes Prezentáció & Interaktív SQL Terminál:** **[https://db-milton.vane.hu](https://db-milton.vane.hu)**
- 🐙 **GitHub Forráskód Repository:** **[https://github.com/Alphaws/db-milton](https://github.com/Alphaws/db-milton)**

---

## 📌 1. A Projekt Áttekintése és Célja

A projekt egy korszerű e-kereskedelmi áruház adatbázisának tervezését és megvalósítását mutatja be, amely **Entity-Attribute-Value (EAV)** sémát alkalmaz a heterogén terméktulajdonságok skálázható tárolására, a 3. normálforma (3NF) szigorú megtartásával.

### Fő komponensek:
- **`sql/webshop_eav_modell.sql`:** 7 normalizált táblát tartalmazó DDL és DML szkript, idegen kulcs kényszerekkel, táblánként 10+ életszerű példasorral és a 4 kötelező típusú tesztlekérdezéssel.
- **Interaktív Webes Bemutató (`index.html`, `assets/css/`, `assets/js/`):** Prezentáció-minőségű, billentyűzetvezérelt slide-deck rendszer a Milton Friedman Egyetem hivatalos arculatával, beépített **élő SQL terminállal** és adatbázis reset funkcióval.
- **PowerPoint Prezentáció (`Webshop_EAV_Adatbazistervezes_Prezentacio.pptx`):** 16:9 szélesvásznú, vizsgakövetelményeknek megfelelő Moodle-feltölthető slide-deck.
- **Dockerizált Mikroarchitektúra:** MariaDB 11.4 adatbázisszerver, Python SQL Runner mikroszerviz, Adminer GUI és Nginx reverse proxy webszerver Traefik integrációval.

---

## 🏛️ 2. Adatbázis Architektúra és Relációk

A rendszer 7 normalizált (3NF) relációból áll:

```
[categories] 1 ────* [products] 1 ────* [product_attribute_values] *──── 1 [attributes]
  (rekurzív)               1
                           │
                           *
                    [order_items] *──── 1 [orders] *──── 1 [customers]
```

### Táblák Specifikációja:
1. **`categories`:** Hierarchikus termékkategóriák önhivatkozó rekurzív idegen kulccsal (`parent_id`).
2. **`products`:** Az EAV minta mag entitása (SKU, név, alap eladási ár, raktárkészlet, státusz).
3. **`attributes`:** A dinamikus műszaki tulajdonságok metaadat katalógusa (kód, név, mértékegység, SQL adattípus).
4. **`product_attribute_values`:** **Összetett elsődleges kulcsos** (`product_id`, `attribute_id`) kapcsolótábla típusbiztos oszlopokkal (`value_varchar`, `value_number`, `value_datetime`).
5. **`customers`:** Vásárlói törzsadatok (név, egyedi email cím, telefonszám, regisztráció dátuma).
6. **`orders`:** Rendelés fejléc dátummal (`order_date`), állapottal (`pending`, `paid`, `shipped`, `cancelled`) és szállítási adatokkal.
7. **`order_items`:** **Összetett elsődleges kulcsos** (`order_id`, `product_id`) kapcsolótábla származtatott kalkulált oszlopokkal (`subtotal = quantity * unit_price STORED`).

---

## ⚡ 3. Tantárgyi Követelmények Teljesülése

| Követelmény | Megvalósítás | Állapot |
|---|---|:---:|
| **Legalább 5-6 tábla** | 7 tábla (`categories`, `products`, `attributes`, `product_attribute_values`, `customers`, `orders`, `order_items`) | ✅ |
| **Normalizálás (legalább 3NF)** | Minden tábla 3NF-ben van (nincs ismétlődő csoport, részleges vagy tranzitív függőség). | ✅ |
| **Legalább 3 mező táblánként** | Minden tábla 5-8 értelmes mezővel rendelkezik. | ✅ |
| **Összetett elsődleges kulcs** | Két táblában is: `product_attribute_values(product_id, attribute_id)` és `order_items(order_id, product_id)`. | ✅ |
| **Dátum mezők** | `created_at`, `registration_date`, `order_date`. | ✅ |
| **PK - FK kapcsolatok** | Szigorú relációs integritás idegen kulcs kényszerekkel (`ON DELETE CASCADE` és `RESTRICT`). | ✅ |
| **Példaadatok** | Minden táblában legalább 10-15 életszerű, valósághű adatsor található. | ✅ |
| **Bachman ábra** | Szabványos, mezőszintű irányított kapcsolatok (1 felől az N felé mutató nyilak). | ✅ |
| **4 típusú mintalekérdezés** | 1. Egytáblás, 2. Függvényes (`COUNT`, `MIN`, `MAX`, `AVG`, `ROUND`, `HAVING`), 3. EAV Pivot JOIN, 4. Allekérdezés (`HAVING SUM > AVG`). | ✅ |

---

## 📁 4. Rendszerezett Projekt Mappastruktúra

```
├── .env.example                               # Minta Docker környezeti változók
├── .dockerignore                              # Docker build kizárások
├── .gitignore                                 # Git kizárások (.env, mariadb_data/)
├── docker-compose.yml                         # Mikroarchitektúra definíció (Traefik routerekkel)
├── Webshop_EAV_Adatbazistervezes_Prezentacio.pptx # Hivatalos beadandó prezentáció (16:9)
├── index.html                                 # 11 diás interaktív prezentáció
├── assets/                                    # Statikus webes eszközök
│   ├── css/
│   │   └── styles.css                         # Prezentációs stíluslap
│   ├── js/
│   │   └── script.js                          # Prezentációs és SQL motor vezérlés
│   └── images/
│       ├── bachman_diagram.png                # Szabványos mezőszintű Bachman ábra
│       └── milton_logo_feher.png              # Milton Friedman Egyetem hivatalos logója
├── sql/
│   └── webshop_eav_modell.sql                 # Hivatalos beadandó DDL/DML SQL állomány
├── src/
│   └── api/
│       └── api_server.py                      # Védett SQL REST API (rate-limiting, timeout, reset)
├── docker/
│   ├── web/
│   │   ├── Dockerfile.web                     # Nginx prezentációs image build
│   │   └── nginx.conf                         # Nginx reverse proxy és routing
│   └── api/
│       └── Dockerfile.api                     # Biztonságos Python SQL Runner build
├── docs/                                      # Háttéranyagok és tanári feladatkiírás
│   ├── kiiras.md
│   ├── sample_bachman.png
│   └── milton_logo_szines.png
└── scripts/                                   # Automatizációs szkriptek
    ├── deploy.sh                              # Éles szerver szinkronizáló és deploy szkript
    ├── generate_bachman_diagram.py            # Matplotlib ábragenerátor
    └── generate_pptx.py                       # Python PPTX generáló szkript
```
