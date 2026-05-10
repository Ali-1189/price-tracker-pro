def clean_price(price_str):
    # أي منطق لتنظيف العملة أو الفواصل
    return float(price_str.replace(',', '').strip())