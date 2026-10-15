"""
IMDb Stealth Browser Engine
Manages a stealth Playwright browser instance with anti-detection capabilities
to bypass AWS WAF, Cloudflare, and bot-detection challenges.
"""

from typing import Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


class StealthBrowser:
    """
    Encapsulates Playwright stealth browser operations for fetching IMDb pages.
    """

    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None

    def _init_browser(self):
        """Initializes browser with stealth flags and user context."""
        if self._playwright is None:
            self._playwright = sync_playwright().start()

        if self._browser is None:
            # Try Chrome first, then Edge, then default Chromium
            browser_launched = False
            for channel in ["chrome", "msedge", None]:
                try:
                    kwargs = {
                        "headless": self.headless,
                        "args": [
                            "--disable-blink-features=AutomationControlled",
                            "--no-sandbox",
                            "--disable-infobars",
                            "--disable-dev-shm-usage",
                            "--disable-extensions",
                        ],
                    }
                    if channel:
                        kwargs["channel"] = channel
                    self._browser = self._playwright.chromium.launch(**kwargs)
                    browser_launched = True
                    break
                except Exception:
                    continue

            if not browser_launched:
                self._browser = self._playwright.chromium.launch(
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"],
                )

        if self._context is None:
            self._context = self._browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                timezone_id="America/New_York",
            )
            # Remove navigator.webdriver property for stealth
            self._context.add_init_script(
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                """
            )

    def get_page_content(self, url: str, wait_selector: Optional[str] = None) -> str:
        """
        Navigates to URL, waits for content or selector, and returns page HTML.
        """
        self._init_browser()
        page: Page = self._context.new_page()
        try:
            page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
            
            # Wait for specific selector if requested or general content
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=12000)
                except Exception:
                    pass
            else:
                # Default wait for main body or header
                try:
                    page.wait_for_selector("script[type='application/ld+json'], h1, ul.ipc-metadata-list", timeout=12000)
                except Exception:
                    pass

            return page.content()
        finally:
            page.close()

    def close(self):
        """Closes browser context and Playwright process."""
        if self._context:
            try:
                self._context.close()
            except Exception:
                pass
            self._context = None

        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None

        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass
            self._playwright = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
