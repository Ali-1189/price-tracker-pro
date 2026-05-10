import logging
import re
from typing import Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ParserError(Exception):
    """Base exception for all parser-related errors."""

class PriceNotFoundError(ParserError):
    """Raised when a price element cannot be located in the HTML."""

class PriceParseError(ParserError):
    """Raised when a price string is found but cannot be converted to a float."""

_NON_NUMERIC_RE = re.compile(r"[^\d.]")

def clean_price(raw: str) -> float:
    if not raw or not raw.strip():
        raise PriceParseError("Received an empty price string.")
    cleaned = raw.strip()
    if re.search(r"\d\.\d{3},\d{2}", cleaned):
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        cleaned = cleaned.replace(",", "")
    cleaned = _NON_NUMERIC_RE.sub("", cleaned)
    if not cleaned:
        raise PriceParseError(f"Could not extract a numeric value: {raw!r}")
    try:
        return float(cleaned)
    except ValueError as exc:
        raise PriceParseError(f"Failed to convert {cleaned!r} to float") from exc

class PriceParser:
    def __init__(self, selector: str):
        self.selector = selector

    def extract_price(self, html_content: str, strict: bool = True) -> float:
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.select_one(self.selector)
        if not element:
            if strict:
                raise PriceNotFoundError(f"Element with selector '{self.selector}' not found.")
            return None
        
        raw_price = element.get_text()
        return clean_price(raw_price)