-- ==============================================================================
-- Milton Friedman Egyetem
-- Kurzus: BH-MIT059-L: Adatbáziskezelés 2.
-- Oktató: Szabó István Gábor
-- Féléves beadandó feladat: Webshop EAV (Entity-Attribute-Value) Termékmodellel
-- Hallgató: Szeness Imre
-- Neptun kód: TQJH7P
-- Félév: 2026/27/1
-- Adatbázis: MariaDB / MySQL 8.0+
-- Karakterkészlet: utf8mb4 / utf8mb4_unicode_ci
-- ==============================================================================

SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS `webshop_eav_db`;
CREATE DATABASE `webshop_eav_db` 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;
USE `webshop_eav_db`;
SET FOREIGN_KEY_CHECKS = 1;

-- ==============================================================================
-- 1. TÁBLÁK LÉTREHOZÁSA (DDL)
-- ==============================================================================

-- 1.1 Kategóriák (Hierarchikus termékkategóriák)
CREATE TABLE `categories` (
    `category_id` INT AUTO_INCREMENT,
    `parent_id` INT NULL,
    `name` VARCHAR(100) NOT NULL,
    `slug` VARCHAR(100) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`category_id`),
    CONSTRAINT `fk_cat_parent` FOREIGN KEY (`parent_id`) 
        REFERENCES `categories` (`category_id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 1.2 Entitás: Termékek alapadatok (Mag entitás az EAV-ban)
CREATE TABLE `products` (
    `product_id` INT AUTO_INCREMENT,
    `category_id` INT NOT NULL,
    `sku` VARCHAR(50) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL,
    `base_price` DECIMAL(12, 2) NOT NULL,
    `stock_qty` INT NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`product_id`),
    CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) 
        REFERENCES `categories` (`category_id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 1.3 Attribútum metaadatok (Az EAV modell "Attribute" eleme)
CREATE TABLE `attributes` (
    `attribute_id` INT AUTO_INCREMENT,
    `code` VARCHAR(50) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `data_type` ENUM('varchar', 'int', 'decimal', 'datetime', 'boolean') NOT NULL,
    `unit` VARCHAR(20) NULL,
    `description` VARCHAR(255) NULL,
    PRIMARY KEY (`attribute_id`)
) ENGINE=InnoDB;

-- 1.4 Termékdinamikus értékek (Az EAV modell "Value" eleme - ÖSSZETETT ELSŐDLEGES KULCCSAL)
CREATE TABLE `product_attribute_values` (
    `product_id` INT NOT NULL,
    `attribute_id` INT NOT NULL,
    `value_varchar` VARCHAR(255) NULL,
    `value_number` DECIMAL(12, 4) NULL,
    `value_datetime` DATETIME NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`product_id`, `attribute_id`),
    CONSTRAINT `fk_pav_product` FOREIGN KEY (`product_id`) 
        REFERENCES `products` (`product_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_pav_attribute` FOREIGN KEY (`attribute_id`) 
        REFERENCES `attributes` (`attribute_id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 1.5 Vásárlók (Ügyfelek adatai)
CREATE TABLE `customers` (
    `customer_id` INT AUTO_INCREMENT,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(30) NULL,
    `registration_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;

-- 1.6 Megrendelések fejléc (Dátum és állapotkezelés)
CREATE TABLE `orders` (
    `order_id` INT AUTO_INCREMENT,
    `customer_id` INT NOT NULL,
    `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `total_amount` DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    `status` ENUM('pending', 'paid', 'shipped', 'cancelled') NOT NULL DEFAULT 'pending',
    `shipping_address` VARCHAR(255) NOT NULL,
    `payment_method` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`order_id`),
    CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 1.7 Megrendelés tételek (ÖSSZETETT ELSŐDLEGES KULCCSAL: order_id, product_id)
CREATE TABLE `order_items` (
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    `unit_price` DECIMAL(12, 2) NOT NULL,
    `subtotal` DECIMAL(12, 2) GENERATED ALWAYS AS (`quantity` * `unit_price`) STORED,
    PRIMARY KEY (`order_id`, `product_id`),
    CONSTRAINT `fk_oi_order` FOREIGN KEY (`order_id`) 
        REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_oi_product` FOREIGN KEY (`product_id`) 
        REFERENCES `products` (`product_id`) ON DELETE RESTRICT
) ENGINE=InnoDB;


-- ==============================================================================
-- 2. PÉLDAADATOK BESZÚRÁSA (DML - Táblánként legalább 10 sor)
-- ==============================================================================

-- 2.1 Kategóriák feltöltése (10 sor)
INSERT INTO `categories` (`category_id`, `parent_id`, `name`, `slug`, `description`) VALUES
(1, NULL, 'Elektronika', 'elektronika', 'Műszaki és elektronikai cikkek főkategória'),
(2, NULL, 'Ruházat és Divat', 'ruhazat-es-divat', 'Férfi, női és gyermek ruházat'),
(3, NULL, 'Otthon és Kert', 'otthon-es-kert', 'Bútorok, konyhafelszerelés, kerti gépek'),
(4, 1, 'Okostelefonok', 'okostelefonok', 'Korszerű mobiltelefonok és phabletek'),
(5, 1, 'Laptopok', 'laptopok', 'Üzleti és gamer hordozható számítógépek'),
(6, 1, 'Audiotechnika', 'audiotechnika', 'Fejhallgatók, hangszórók, erősítők'),
(7, 2, 'Férfi cipők', 'ferfi-cipok', 'Utcai és sportcipők férfiaknak'),
(8, 2, 'Női kabátok', 'noi-kabatok', 'Átmeneti és téli női kabátok'),
(9, 3, 'Kávéfőzők', 'kavefozok', 'Eszpresszó és automata kávégépek'),
(10, 3, 'Irodai székek', 'irodai-szekek', 'Ergonomikus székek munkához');

-- 2.2 Attribútumok (EAV metaadatok - 10 sor)
INSERT INTO `attributes` (`attribute_id`, `code`, `name`, `data_type`, `unit`, `description`) VALUES
(1, 'color', 'Szín', 'varchar', NULL, 'Termék domináns színe'),
(2, 'storage_capacity', 'Belső tárhely', 'int', 'GB', 'Háttértár kapacitása'),
(3, 'ram_size', 'Memória mérete', 'int', 'GB', 'Rendszermemória (RAM)'),
(4, 'weight_kg', 'Súly', 'decimal', 'kg', 'Termék tömege'),
(5, 'screen_diagonal', 'Kijelző átmérő', 'decimal', 'col', 'Kijelző képátlója hüvelykben'),
(6, 'shoe_size', 'Cipőméret', 'decimal', 'EU', 'Európai szabványú méret'),
(7, 'material', 'Anyagösszetétel', 'varchar', NULL, 'Főbb felhasznált anyagok'),
(8, 'warranty_months', 'Garancia időtartama', 'int', 'hónap', 'Gyári garancia hónapokban'),
(9, 'power_watt', 'Teljesítmény', 'int', 'W', 'Elektromos fogyasztás/teljesítmény'),
(10, 'release_date', 'Kiadás éve/napja', 'datetime', NULL, 'Piacra kerülés időpontja');

-- 2.3 Termékek (10 sor)
INSERT INTO `products` (`product_id`, `category_id`, `sku`, `name`, `base_price`, `stock_qty`, `is_active`, `created_at`) VALUES
(1, 4, 'PHN-APL-15P', 'iPhone 15 Pro 128GB', 419990.00, 15, 1, '2026-01-10 09:30:00'),
(2, 4, 'PHN-SAM-S24', 'Samsung Galaxy S24', 359900.00, 22, 1, '2026-01-15 11:20:00'),
(3, 5, 'NB-DEL-XPS15', 'Dell XPS 15 9530', 789000.00, 8, 1, '2026-02-01 14:00:00'),
(4, 5, 'NB-LEN-T14', 'Lenovo ThinkPad T14 Gen 4', 540000.00, 12, 1, '2026-02-10 10:15:00'),
(5, 6, 'AUD-SNY-WH1000', 'Sony WH-1000XM5 Fejhallgató', 129990.00, 35, 1, '2026-02-18 16:45:00'),
(6, 7, 'SH-NKE-AM90', 'Nike Air Max 90', 48990.00, 40, 1, '2026-03-01 08:00:00'),
(7, 7, 'SH-ADI-UB23', 'Adidas Ultraboost Light', 59990.00, 25, 1, '2026-03-05 13:30:00'),
(8, 8, 'CL-COL-WTR24', 'Columbia Téli Pehelykabát', 74990.00, 18, 1, '2026-03-12 17:10:00'),
(9, 9, 'KIT-DLG-EC685', 'DeLonghi Dedica Kávéfőző', 64990.00, 14, 1, '2026-03-20 12:00:00'),
(10, 10, 'FUR-HM-AER', 'Herman Miller Aeron Szék', 499000.00, 5, 1, '2026-04-01 15:20:00');

-- 2.4 EAV Értékek (product_attribute_values - 15+ sor)
INSERT INTO `product_attribute_values` (`product_id`, `attribute_id`, `value_varchar`, `value_number`, `value_datetime`, `created_at`) VALUES
-- iPhone 15 Pro
(1, 1, 'Titán natúr', NULL, NULL, '2026-01-10 10:00:00'),
(1, 2, NULL, 128.0000, NULL, '2026-01-10 10:00:00'),
(1, 3, NULL, 8.0000, NULL, '2026-01-10 10:00:00'),
(1, 5, NULL, 6.1000, NULL, '2026-01-10 10:00:00'),
(1, 8, NULL, 24.0000, NULL, '2026-01-10 10:00:00'),
-- Samsung Galaxy S24
(2, 1, 'Ónixfekete', NULL, NULL, '2026-01-15 11:30:00'),
(2, 2, NULL, 256.0000, NULL, '2026-01-15 11:30:00'),
(2, 5, NULL, 6.2000, NULL, '2026-01-15 11:30:00'),
-- Dell XPS 15
(3, 1, 'Ezüst', NULL, NULL, '2026-02-01 14:10:00'),
(3, 2, NULL, 1024.0000, NULL, '2026-02-01 14:10:00'),
(3, 3, NULL, 32.0000, NULL, '2026-02-01 14:10:00'),
(3, 4, NULL, 1.8600, NULL, '2026-02-01 14:10:00'),
-- Sony WH-1000XM5
(5, 1, 'Ezüstös fehér', NULL, NULL, '2026-02-18 17:00:00'),
(5, 4, NULL, 0.2500, NULL, '2026-02-18 17:00:00'),
-- Nike Air Max
(6, 1, 'Fekete/Fehér', NULL, NULL, '2026-03-01 08:30:00'),
(6, 6, NULL, 43.5000, NULL, '2026-03-01 08:30:00'),
(6, 7, 'Bőr és szintetikus textil', NULL, NULL, '2026-03-01 08:30:00'),
-- DeLonghi Kávéfőző
(9, 1, 'Piros fém', NULL, NULL, '2026-03-20 12:30:00'),
(9, 9, NULL, 1300.0000, NULL, '2026-03-20 12:30:00'),
(9, 8, NULL, 36.0000, NULL, '2026-03-20 12:30:00');

-- 2.5 Vásárlók feltöltése (10 sor)
INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`, `registration_date`) VALUES
(1, 'Gábor', 'Kovács', 'kovacs.gabor@example.hu', '+36201112233', '2026-01-05 14:22:00'),
(2, 'Anna', 'Nagy', 'nagy.anna@example.hu', '+36302223344', '2026-01-12 09:15:00'),
(3, 'Péter', 'Szabó', 'szabo.peter@example.hu', '+36703334455', '2026-01-20 18:40:00'),
(4, 'Zsuzsanna', 'Tóth', 'toth.zsuzsa@example.hu', '+36204445566', '2026-02-02 11:05:00'),
(5, 'Tamás', 'Horváth', 'horvath.tamas@example.hu', '+36305556677', '2026-02-14 16:30:00'),
(6, 'Katalin', 'Varga', 'varga.katalin@example.hu', '+36706667788', '2026-02-25 10:50:00'),
(7, 'Bence', 'Kiss', 'kiss.bence@example.hu', '+36207778899', '2026-03-03 13:12:00'),
(8, 'Dóra', 'Molnár', 'molnar.dora@example.hu', '+36308889900', '2026-03-15 17:45:00'),
(9, 'Máté', 'Farkas', 'farkas.mate@example.hu', '+36709990011', '2026-03-22 08:20:00'),
(10, 'Eszter', 'Balogh', 'balogh.eszter@example.hu', '+36200001122', '2026-04-05 19:10:00');

-- 2.6 Megrendelések fejléc feltöltése (10 sor)
INSERT INTO `orders` (`order_id`, `customer_id`, `order_date`, `total_amount`, `status`, `shipping_address`, `payment_method`) VALUES
(1, 1, '2026-02-01 10:15:00', 419990.00, 'shipped', '1117 Budapest, Október 23. u. 12.', 'bankcard'),
(2, 2, '2026-02-05 14:30:00', 540000.00, 'paid', '4025 Debrecen, Piac utca 45.', 'transfer'),
(3, 3, '2026-02-12 11:00:00', 178980.00, 'shipped', '6720 Szeged, Tisza Lajos krt. 18.', 'bankcard'),
(4, 4, '2026-02-20 16:20:00', 74990.00, 'paid', '9021 Győr, Baross Gábor út 8.', 'cash_on_delivery'),
(5, 5, '2026-03-02 09:45:00', 789000.00, 'shipped', '7621 Pécs, Király utca 3.', 'transfer'),
(6, 6, '2026-03-10 13:10:00', 64990.00, 'pending', '3525 Miskolc, Széchenyi u. 52.', 'bankcard'),
(7, 7, '2026-03-18 18:00:00', 108980.00, 'paid', '8000 Székesfehérvár, Várkörút 14.', 'bankcard'),
(8, 8, '2026-03-25 12:40:00', 499000.00, 'cancelled', '9700 Szombathely, Fő tér 6.', 'transfer'),
(9, 1, '2026-04-02 15:30:00', 129990.00, 'shipped', '1117 Budapest, Október 23. u. 12.', 'bankcard'),
(10, 9, '2026-04-10 17:15:00', 359900.00, 'pending', '2800 Tatabánya, Komáromi út 21.', 'cash_on_delivery');

-- 2.7 Megrendelés tételek feltöltése (order_items - 12 sor)
INSERT INTO `order_items` (`order_id`, `product_id`, `quantity`, `unit_price`) VALUES
(1, 1, 1, 419990.00),
(2, 4, 1, 540000.00),
(3, 5, 1, 129990.00),
(3, 6, 1, 48990.00),
(4, 8, 1, 74990.00),
(5, 3, 1, 789000.00),
(6, 9, 1, 64990.00),
(7, 6, 1, 48990.00),
(7, 7, 1, 59990.00),
(8, 10, 1, 499000.00),
(9, 5, 1, 129990.00),
(10, 2, 1, 359900.00);


-- ==============================================================================
-- 3. KÖVETELMÉNYEKNEK MEGFELELŐ LEKÉRDEZÉSEK ÉS EREDMÉNYEK
-- ==============================================================================

-- 3.1 Egyszerű egytáblás lekérdezés:
-- Aktív termékek listázása alapár szerinti csökkenő sorrendben
SELECT 
    product_id, 
    sku, 
    name, 
    base_price, 
    stock_qty
FROM products
WHERE is_active = 1
ORDER BY base_price DESC;

-- 3.2 Értelmes függvényhasználatot bemutató lekérdezés:
-- Kategóriánkénti aggregáció (termékszám, legolcsóbb, legdrágább és átlagos termékár formázva)
SELECT 
    c.name AS kategoria_nev,
    COUNT(p.product_id) AS termek_db,
    MIN(p.base_price) AS legolcsobb_ar_huf,
    MAX(p.base_price) AS legdragabb_ar_huf,
    ROUND(AVG(p.base_price), 2) AS atlagos_ar_huf
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.name
HAVING termek_db > 0
ORDER BY atlagos_ar_huf DESC;

-- 3.3 Összetett, többtáblás lekérdezés értelmes szűréssel (EAV Pivot + Megrendelések):
-- Kilistázza a 'shipped' vagy 'paid' státuszú rendelések tételeit a vásárló nevével, 
-- a megrendelt termékkel és annak EAV-ból kinyert színével és tárhelyével.
SELECT 
    o.order_id,
    o.order_date,
    CONCAT(c.last_name, ' ', c.first_name) AS vasarlo_neve,
    p.name AS termek_neve,
    oi.quantity AS darab,
    oi.unit_price AS egysegar,
    oi.subtotal AS tetel_osszesen,
    COALESCE(pav_color.value_varchar, 'Nincs megadva') AS szin,
    CONCAT(COALESCE(pav_storage.value_number, 0), ' GB') AS tarhely
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_attribute_values pav_color 
    ON p.product_id = pav_color.product_id 
    AND pav_color.attribute_id = (SELECT attribute_id FROM attributes WHERE code = 'color' LIMIT 1)
LEFT JOIN product_attribute_values pav_storage 
    ON p.product_id = pav_storage.product_id 
    AND pav_storage.attribute_id = (SELECT attribute_id FROM attributes WHERE code = 'storage_capacity' LIMIT 1)
WHERE o.status IN ('paid', 'shipped')
ORDER BY o.order_date DESC;

-- 3.4 Allekérdezést (Subquery) tartalmazó lekérdezés:
-- Azon vásárlók lekérdezése, akiknek az összesített rendelési értéke meghaladja az átlagos rendelési értéket.
SELECT 
    c.customer_id,
    CONCAT(c.last_name, ' ', c.first_name) AS vasarlo_neve,
    c.email,
    COUNT(o.order_id) AS leadott_rendelesek_szama,
    SUM(o.total_amount) AS osszes_koltes_huf
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.last_name, c.first_name, c.email
HAVING SUM(o.total_amount) > (
    -- Allekérdezés: az összes érvényes rendelés átlagos összege
    SELECT AVG(total_amount) 
    FROM orders 
    WHERE status <> 'cancelled'
)
ORDER BY osszes_koltes_huf DESC;
