"""
app/scraper/scraper.py

Responsible for fetching raw HTML content from URLs.
Parsing logic is intentionally excluded and belongs in parser.py.
"""

import logging
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    TooManyRedirects,
    HTTPError,
    RequestException,
)

# Configure module-level logger
logger = logging.getLogger(__name__)

# Default headers to mimic a real browser visit
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DEFAULT_TIMEOUT = 10  # seconds


class ScraperError(Exception):
    """Base exception for all scraper-related errors."""


class FetchError(ScraperError):
    """Raised when a URL cannot be fetched due to network or HTTP issues."""


class Scraper:
    """
    Handles HTTP requests to fetch raw HTML content from URLs.

    Parsing logic is NOT included here — see parser.py.

    Usage:
        scraper = Scraper()
        html = scraper.fetch("https://example.com")
    """

    def __init__(
        self,
        headers: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
    ):
        """
        Initialise the Scraper.

        Args:
            headers:      Custom HTTP headers. Merged on top of DEFAULT_HEADERS.
            timeout:      Request timeout in seconds.
            max_retries:  Number of retry attempts on transient failures.
        """
        self.timeout = timeout
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Attach a retry adapter for transient network failures
        retry_adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount("http://", retry_adapter)
        self.session.mount("https://", retry_adapter)

    def fetch(self, url: str) -> str:
        """
        Fetch the raw HTML content of a URL.

        Args:
            url: The target URL to fetch.

        Returns:
            The response body as a decoded string.

        Raises:
            FetchError: On any network or HTTP-level failure.
        """
        logger.info("Fetching URL: %s", url)

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # Raise on 4xx / 5xx status codes

        except ConnectionError as exc:
            raise FetchError(f"Failed to connect to '{url}': {exc}") from exc

        except Timeout as exc:
            raise FetchError(
                f"Request timed out after {self.timeout}s for '{url}': {exc}"
            ) from exc

        except TooManyRedirects as exc:
            raise FetchError(f"Too many redirects for '{url}': {exc}") from exc

        except HTTPError as exc:
            raise FetchError(
                f"HTTP error {response.status_code} for '{url}': {exc}"
            ) from exc

        except RequestException as exc:
            # Catch-all for any other requests-related error
            raise FetchError(f"Unexpected request error for '{url}': {exc}") from exc

        logger.info(
            "Successfully fetched '%s' [status=%s, size=%d bytes]",
            url,
            response.status_code,
            len(response.content),
        )

        return response.text

    def close(self) -> None:
        """Release the underlying connection pool."""
        self.session.close()
        logger.debug("Scraper session closed.")

    # Allow use as a context manager: `with Scraper() as s:`
    def __enter__(self) -> "Scraper":
        return self

    def __exit__(self, *_) -> None:
        self.close()