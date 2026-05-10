# app/scraper/selectors.py

SITE_CONFIGS = {
    "amazon": {
        "price": "span.a-price-whole, span.priceToPay, span.a-offscreen",
        "title": "#productTitle",
        "clean_logic": "amazon_clean"
    },
    "noon": {
        "price": ".priceNow",
        "title": "h1",
        "clean_logic": "standard"
    },
    "jumia": {
        "price": ".-prc",
        "title": ".-fs20",
        "clean_logic": "standard"
    }
}