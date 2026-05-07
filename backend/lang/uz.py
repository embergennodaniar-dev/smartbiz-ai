# ============================================================
#  lang/qq.py  — Barcha qoraqalpoqcha matnlar shu yerda!
#  Ishlatish: from lang.qq import T, f
# ============================================================

T: dict[str, str] = {

    # ── Xato xabarlari ──────────────────────────────────────
    "store_not_found":       "Dúkan tabılmadı",
    "sale_not_found":        "Sawda tabılmadı",
    "product_not_found":     "Ónim tabılmadı",
    "debt_not_found":        "Qarız tabılmadı",
    "csv_only":              "Tek CSV faylı qabıl etiledi",
    "col_missing":           "'date' hám 'total' baǵanaları tabılmadı",

    # ── Muvaffaqiyat ────────────────────────────────────────
    "saved":                 "Saqlandı!",
    "deleted":               "Óshirildi",
    "paid":                  "Tólew jazıldı!",

    # ── Auth xatolar ────────────────────────────────────────
    "email_exists":          "Bul email aldın dizimnen ótken",
    "invalid_credentials":   "Email yaki parol nadurıs",
    "token_expired":         "Sessiya waqtı tawsıldı, qaytadan kiriń",
    "token_invalid":         "Ruxsat joq",
    "not_authenticated":     "Iltimas, aldın sistemaǵa kiriń",
    "register_success":      "Tabıslı dizimnen óttińiz!",
    "logout_success":        "Sistemanan shıqtıńız",
    "password_mismatch":     "Parollar sáykes kelmedi",
    "password_short":        "Parol keminde 6 belgi bolıwı kerek",
    "field_required":        "Bul orın toltırılıwı shárt",

    # ── Auth UI ─────────────────────────────────────────────
    "auth_brand":            "SmartBiz AI",
    "auth_tagline":          "Biznesińizdi aqıllı basqarıń",
    "login_title":           "Xosh keldińiz!",
    "login_subtitle":        "Akkauntıńızǵa kiriń",
    "register_title":        "Baslań!",
    "register_subtitle":     "Biyul akkaunt jaratıń",
    "label_fullname":        "Tolıq atıńız",
    "label_email":           "Email mánzil",
    "label_password":        "Parol",
    "label_confirm":         "Paroldi tastıyıqlań",
    "label_store_name":      "Dúkan atı",
    "label_store_type":      "Dúkan túri",
    "btn_login":             "Kiriw",
    "btn_register":          "Akkaunt jaratıw",
    "btn_logout":            "Shıǵıw",
    "btn_loading":           "Júklenmekte...",
    "link_to_register":      "Akkauntıńız joqpa? Dizimnen ótiń ->",
    "link_to_login":         "Akkauntıńız barma? Kiriń ->",
    "ph_fullname":           "Atı Familiyası",
    "ph_email":              "siziń@email.com",
    "ph_password":           "Keminde 6 belgi",
    "ph_store":              "Mısalı: Tiykarǵı dúkan",
    "store_type_dokon":      "Dúkan",
    "store_type_restoran":   "Restoran",
    "store_type_filial":     "Filial",
    "store_type_ombor":      "Ammar",

    # ── Dashboard ────────────────────────────────────────────
    "greeting_morning":      "Qayırlı tań",
    "greeting_day":          "Qayırlı kún",
    "greeting_evening":      "Qayırlı kesh",

    # ── Hafta kunlari ────────────────────────────────────────
    "day_mon":               "Dúyshembi",
    "day_tue":               "Siyshembi",
    "day_wed":               "Sárshembi",
    "day_thu":               "Piyshembi",
    "day_fri":               "Juma",
    "day_sat":               "Shembi",
    "day_sun":               "Ekshembi",

    # ── Demo data ────────────────────────────────────────────
    "demo_store_name":       "Meniń Dúkanım",
    "demo_store_type":       "dúkan",
    "demo_store_address":    "Tashkent",
    "prod_bread":            "Nan",
    "prod_milk":             "Sút",
    "prod_meat":             "Gósh",
    "prod_sugar":            "Qant",
    "prod_oil":              "May",
    "prod_cheese":           "Sır",
    "prod_rice":             "Gúrish",
    "prod_flour":            "Un",
    "prod_egg":              "Máyek",
    "prod_sausage":          "Kolbasa",
    "prod_fish":             "Balıq",
    "prod_cat_food":         "azıq-awqat",
    "prod_unit_kg":          "kg",
    "prod_unit_litr":        "litr",
    "prod_unit_dona":        "dana",
    "demo_debt_1_name":      "Alisher Karimov",
    "demo_debt_1_phone":     "998901234567",
    "demo_debt_2_name":      "Nodira Yusupova",
    "demo_debt_2_phone":     "998901234568",
    "demo_debt_3_name":      "Batır Raximov",
    "demo_debt_3_phone":     "998901234569",
    "demo_debt_4_name":      "Kótere baza",
    "demo_debt_4_phone":     "998712345678",
    "debt_type_client":      "qarıydar",
    "debt_type_supplier":    "jetkerip beriwshi",

    # ── AI Insights ──────────────────────────────────────────
    "insight_stock_low_title":    "{name} kem qaldı",
    "insight_debt_overdue_title": "{person} - múddeti ótken qarız",
    "insight_best_day_title":     "{day} - eń aktiv kún",
    "insight_growth_title":       "Ótken háptege qaraǵanda +{pct}% ósiw",
    "insight_drop_title":         "Sawda {pct}% tómenledi",
    "insight_top_products_title": "Eń kóp satılatuǵın ónimler",
    "insight_stock_low_text":     "Házir {qty} {unit} qaldı, minimum {min_qty}. Zapastı toltırıń.",
    "insight_debt_overdue_text":  "{amount} sum qarız múddeti ótti. Eskertiw jiberiń.",
    "insight_best_day_text":      "Ortasha {avg} sum sawda. Bul kúni xızmetkerdi kóbeytiń.",
    "insight_growth_text":        "Sawdanıń ósiw tendenciyası dawam etpekte. Zapastı asırıń.",
    "insight_drop_text":          "Bul hápte sawda kemeydi. Akciya ótkeriwdi oylap kóriń.",
    "insight_top_products_text":  "Nan, sút hám qant joqarı talapta. Zapas tawsılmasın.",

    # ── Upload ───────────────────────────────────────────────
    "upload_sales_ok":       "{count} sawda tabıslı júklendi",
    "upload_products_ok":    "{count} ónim júklendi",
    "upload_row_error":      "Qatar {row}: {err}",
    "csv_sales_sample":      "date,total,cash,card,expenses,customers\n2025-01-15,2500000,1500000,1000000,750000,85\n",
    "csv_products_sample":   "name,category,unit,quantity,min_quantity,buy_price,sell_price\nNan,azıq-awqat,kg,100,10,3500,5000\n",
    "csv_sales_filename":    "sawda_shablon.csv",
    "csv_products_filename": "onim_shablon.csv",

    # ── Gemini AI ────────────────────────────────────────────
    "ai_system_prompt": (
        "Sen SmartBiz AI - qaraqalpaq biznes járdemshisisen. "
        "Tek qaraqalpaq tilinde juwap ber. "
        "Paydalanıwshı dúkan maǵlıwmatları tiykarında anıq, qısqa, ámeliy másláhát ber. "
        "Hár dayım unamlı hám professional bol. "
        "Sanlardı sum hám dana da jaz. "
        "Juwap 3-5 gápten aspasın. Dizim ornına áddiy gáp islet."
    ),
    "ai_report_prompt": (
        "Tómendegi biznes maǵlıwmatları tiykarında aylıq esabat jaz (qaraqalpaq tilinde):\n"
        "{data}\n\n"
        "Esabatta bolsın: ulıwma nátiyje, eń jaqsı hám jaman tárepler, "
        "3 anıq usınıs. Jámi 150-200 sóz. Rásmiy biznes stilinde."
    ),
    "ai_chat_context": (
        "Dúkan: {store_name}\n"
        "Búgingi sawda: {today} sum\n"
        "Aylıq sawda: {monthly} sum\n"
        "Top ónim: {top_product}\n"
        "Kem qalǵan: {low_stock}\n"
        "Ótken qarızlar: {overdue_debts} ta\n\n"
        "Soraw: {question}"
    ),
    "ai_key_missing":        "Gemini API giliti tabılmadı. .env ǵa GEMINI_API_KEY= qosıń.",
    "ai_error":              "AI házir islemeyaptı, keyinrek urınıp kóriń.",
    "ai_chat_placeholder":   "Dúkanıńız haqqında soraw beriń...",
    "ai_chat_title":         "AI Járdemshi",
    "ai_report_title":       "AI Aylıq Esabat",
    "ai_report_generating":  "AI esabat tayarlamaqta...",
    "ai_send":               "Jiberiw",
    "ai_welcome": (
        "Sálem! Men siziń biznes járdemshińizben. "
        "Sawda, ónimler, qarızlar yaki prognoz haqqında "
        "qálegen sorawıńızdı beriń."
    ),
    "ai_settings_title":     "AI Sazlamaları",
    "ai_key_label":          "Gemini API gilit",
    "ai_key_placeholder":    "AIzaSy...",
    "ai_key_save":           "Saqlaw",
    "ai_key_saved":          "API gilit saqlandı!",
    "ai_powered":            "Gemini AI tárepinen",
}


def f(key: str, **kwargs) -> str:
    """Kalit bo'yicha matn olib, o'zgaruvchilarni qo'yadi."""
    template = T.get(key, key)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


WEEKDAYS: list[str] = [
    T["day_mon"], T["day_tue"], T["day_wed"], T["day_thu"],
    T["day_fri"], T["day_sat"], T["day_sun"],
]

WEEKDAY_BY_DOW: dict[int, str] = {
    0: T["day_sun"], 1: T["day_mon"], 2: T["day_tue"], 3: T["day_wed"],
    4: T["day_thu"], 5: T["day_fri"], 6: T["day_sat"],
}