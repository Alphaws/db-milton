import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_bachman_diagram():
    # Vászon beállítása (16:9 arány, nagy felbontás)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#0b0f19') # Mély sötétkék háttér
    ax.set_facecolor('#0b0f19')

    # Koordináta határok: 0 - 100 x, 0 - 100 y
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Színek
    C_ENTITY_BG = '#151d30'
    C_HEADER_BG = '#1e293b'
    C_BORDER = '#38bdf8'       # Világoskék szegély
    C_BORDER_EAV = '#f59e0b'   # Borostyán az EAV összetett kulcshoz
    C_BORDER_ORDER = '#ec4899' # Rózsaszín a rendelés alrendszerhez
    C_TEXT_TITLE = '#ffffff'
    C_TEXT_PK = '#f87171'      # Pirosas PK
    C_TEXT_FK = '#38bdf8'      # Kék FK
    C_TEXT_ATTR = '#cbd5e1'    # Fehéresszürke normál mezők
    C_LINE = '#94a3b8'         # Kapcsolati vonalak

    def draw_entity(x, y, w, h, title, fields, border_color=C_BORDER, is_composite=False):
        # Fő kártya doboz
        rect = patches.FancyBboxPatch((x, y), w, h,
                                      boxstyle="round,pad=0.2,rounding_size=1.0",
                                      linewidth=2, edgecolor=border_color,
                                      facecolor=C_ENTITY_BG, zorder=2)
        ax.add_patch(rect)

        # Fejléc háttér
        header_h = 3.8
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                             boxstyle="round,pad=0.2,rounding_size=1.0",
                                             linewidth=1, edgecolor=border_color,
                                             facecolor=header_color if 'header_color' in locals() else C_HEADER_BG, zorder=3)
        ax.add_patch(header_rect)

        # Fejléc elválasztó egyenes vonal
        ax.plot([x, x + w], [y + h - header_h, y + h - header_h], color=border_color, lw=1.5, zorder=4)

        # Cím szöveg
        ax.text(x + w / 2, y + h - header_h / 2, title,
                ha='center', va='center', color=C_TEXT_TITLE,
                fontsize=11, fontweight='bold', fontfamily='sans-serif', zorder=5)

        # Mezők kiírása
        cur_y = y + h - header_h - 1.8
        for field in fields:
            f_type = field.get('type', 'attr')
            name = field['name']
            
            # Kulcs prefix jelölés
            if f_type == 'pk':
                prefix = "# (PK) "
                color = C_TEXT_PK
                weight = 'bold'
            elif f_type == 'fk':
                prefix = "* (FK) "
                color = C_TEXT_FK
                weight = 'bold'
            elif f_type == 'pk_fk':
                prefix = "#* (PK,FK) "
                color = '#fbbf24'
                weight = 'bold'
            else:
                prefix = "  "
                color = C_TEXT_ATTR
                weight = 'normal'

            ax.text(x + 1.2, cur_y, prefix + name,
                    ha='left', va='center', color=color,
                    fontsize=8.5, fontweight=weight, fontfamily='monospace', zorder=5)
            cur_y -= 2.2

    # --- ENTITÁSOK POZICIONÁLÁSA (Bachman 7 tábla) ---

    # FELSŐ SOR: EAV TERMÉKKATALÓGUS
    # 1. categories
    draw_entity(4, 56, 18, 28, "CATEGORIES", [
        {'name': 'category_id', 'type': 'pk'},
        {'name': 'parent_id', 'type': 'fk'},
        {'name': 'name', 'type': 'attr'},
        {'name': 'slug', 'type': 'attr'},
        {'name': 'description', 'type': 'attr'},
        {'name': 'created_at', 'type': 'attr'}
    ], C_BORDER)

    # 2. products (Mag Entitás)
    draw_entity(36, 54, 21, 32, "PRODUCTS (Entity)", [
        {'name': 'product_id', 'type': 'pk'},
        {'name': 'category_id', 'type': 'fk'},
        {'name': 'sku', 'type': 'attr'},
        {'name': 'name', 'type': 'attr'},
        {'name': 'base_price', 'type': 'attr'},
        {'name': 'stock_qty', 'type': 'attr'},
        {'name': 'is_active', 'type': 'attr'},
        {'name': 'created_at', 'type': 'attr'}
    ], C_BORDER)

    # 3. product_attribute_values (EAV Összetett kulcsos értékek)
    draw_entity(67, 56, 28, 28, "PROD_ATTR_VALUES (Value)", [
        {'name': 'product_id', 'type': 'pk_fk'},
        {'name': 'attribute_id', 'type': 'pk_fk'},
        {'name': 'value_varchar', 'type': 'attr'},
        {'name': 'value_number', 'type': 'attr'},
        {'name': 'value_datetime', 'type': 'attr'},
        {'name': 'created_at', 'type': 'attr'}
    ], C_BORDER_EAV)

    # 4. attributes (EAV Metaadatok - fent jobbra)
    draw_entity(70, 12, 25, 28, "ATTRIBUTES (Attribute)", [
        {'name': 'attribute_id', 'type': 'pk'},
        {'name': 'code', 'type': 'attr'},
        {'name': 'name', 'type': 'attr'},
        {'name': 'data_type', 'type': 'attr'},
        {'name': 'unit', 'type': 'attr'},
        {'name': 'description', 'type': 'attr'}
    ], C_BORDER_EAV)

    # ALSÓ SOR: VÁSÁRLÓK ÉS MEGRENDELÉSEK
    # 5. customers
    draw_entity(4, 12, 18, 28, "CUSTOMERS", [
        {'name': 'customer_id', 'type': 'pk'},
        {'name': 'first_name', 'type': 'attr'},
        {'name': 'last_name', 'type': 'attr'},
        {'name': 'email', 'type': 'attr'},
        {'name': 'phone', 'type': 'attr'},
        {'name': 'registration_date', 'type': 'attr'}
    ], C_BORDER_ORDER)

    # 6. orders (Rendelés Fejléc)
    draw_entity(30, 12, 19, 30, "ORDERS", [
        {'name': 'order_id', 'type': 'pk'},
        {'name': 'customer_id', 'type': 'fk'},
        {'name': 'order_date', 'type': 'attr'},
        {'name': 'total_amount', 'type': 'attr'},
        {'name': 'status', 'type': 'attr'},
        {'name': 'shipping_address', 'type': 'attr'},
        {'name': 'payment_method', 'type': 'attr'}
    ], C_BORDER_ORDER)

    # 7. order_items (Rendelés Tételek - Összetett kulcs)
    draw_entity(53, 12, 14, 25, "ORDER_ITEMS", [
        {'name': 'order_id', 'type': 'pk_fk'},
        {'name': 'product_id', 'type': 'pk_fk'},
        {'name': 'quantity', 'type': 'attr'},
        {'name': 'unit_price', 'type': 'attr'},
        {'name': 'subtotal', 'type': 'attr'}
    ], C_BORDER_ORDER)

    # --- BACHMAN NYILAK RAJZOLÁSA (1 : N Irányított kapcsolatok) ---
    # Szabály: Az 1 felől indul, és a nyílhegy az N (több) felé mutat!
    def draw_bachman_arrow(x_start, y_start, x_end, y_end, label="", label_pos=None):
        arrow = patches.FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        arrowstyle='-|>',
                                        mutation_scale=16,
                                        lw=2, color='#38bdf8', zorder=6)
        ax.add_patch(arrow)
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label,
                    ha='center', va='center', color='#94a3b8',
                    fontsize=8.5, fontweight='bold', fontfamily='sans-serif',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#0b0f19', edgecolor='#1e293b', lw=1),
                    zorder=7)

    # 1. categories (1) -> products (N)
    draw_bachman_arrow(22, 70, 36, 70, "1 : N", (29, 72.5))

    # 2. products (1) -> product_attribute_values (N)
    draw_bachman_arrow(57, 70, 67, 70, "1 : N", (62, 72.5))

    # 3. attributes (1) -> product_attribute_values (N)
    draw_bachman_arrow(82.5, 40, 82.5, 56, "1 : N", (85.5, 48))

    # 4. customers (1) -> orders (N)
    draw_bachman_arrow(22, 26, 30, 26, "1 : N", (26, 28.5))

    # 5. orders (1) -> order_items (N)
    draw_bachman_arrow(49, 24, 53, 24, "1 : N", (51, 26.5))

    # 6. products (1) -> order_items (N) (Felülről lefelé)
    draw_bachman_arrow(46.5, 54, 58, 37, "1 : N", (55, 46))

    # 7. categories rekurzió (parent_id)
    # Rajzolunk egy kis hurkot categories felett
    arc = patches.FancyArrowPatch((10, 84), (16, 84),
                                  connectionstyle="arc3,rad=-1.2",
                                  arrowstyle='-|>', mutation_scale=14,
                                  lw=1.8, color='#38bdf8', zorder=6)
    ax.add_patch(arc)
    ax.text(13, 91, "1:N (parent)", ha='center', va='center', color='#94a3b8', fontsize=7.5, zorder=7)

    # Diagram címe és jelmagyarázat
    ax.text(50, 96, "WEBSHOP EAV LOGIKAI ADATMODELL — BACHMAN ÁBRA",
            ha='center', va='center', color='#ffffff', fontsize=16, fontweight='bold', fontfamily='sans-serif')
    ax.text(50, 92.5, "Bachman-konvenció: Irányított nyíl mutat az 1-oldaltól a több (N) kapcsolat felé. Összetett kulcsok: (PK, FK)",
            ha='center', va='center', color='#38bdf8', fontsize=10, fontfamily='sans-serif')

    out_file = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "bachman_diagram.png")
    plt.tight_layout()
    plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Bachman diagram kép sikeresen generálva:", out_file)

if __name__ == "__main__":
    draw_bachman_diagram()
