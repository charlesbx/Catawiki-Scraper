"""
Browser automation manager for web scraping.
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from src.config.settings import CHROME_BINARY, CHROMEDRIVER_BINARY, HEADLESS_MODE
from src.utils.logger import logger


class BrowserManager:
    """
    Manages Chrome/Chromium browser instances for scraping.
    """

    def __init__(
        self,
        headless: bool = None,
        chrome_binary: Optional[str] = None,
        chromedriver_binary: Optional[str] = None,
    ):
        """
        Initialize browser manager.

        Args:
            headless: Run in headless mode (uses config default if None)
            chrome_binary: Path to Chrome/Chromium binary
            chromedriver_binary: Path to ChromeDriver binary
        """
        self.headless = headless if headless is not None else HEADLESS_MODE
        self.chrome_binary = chrome_binary or CHROME_BINARY
        self.chromedriver_binary = chromedriver_binary or CHROMEDRIVER_BINARY
        self._driver: Optional[webdriver.Chrome] = None

    def get_driver(self) -> webdriver.Chrome:
        """
        Get or create a Chrome driver instance.

        Returns:
            Configured Chrome WebDriver

        Raises:
            WebDriverException: If driver initialization fails
        """
        if self._driver is None:
            self._driver = self._create_driver()
        return self._driver

    def _create_driver(self) -> webdriver.Chrome:
        """
        Create a new Chrome driver with configured options.

        Returns:
            New Chrome WebDriver instance
        """
        options = Options()

        # Headless mode
        if self.headless:
            options.add_argument("--headless=new")
            logger.debug("Browser running in headless mode")

        # Performance optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Disable images for faster loading (optional)
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        # Set binary location if specified
        if self.chrome_binary:
            options.binary_location = self.chrome_binary

        # User agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        try:
            # Create service if chromedriver path specified
            if self.chromedriver_binary:
                service = Service(executable_path=self.chromedriver_binary)
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)

            logger.info("Browser driver initialized successfully")
            return driver

        except WebDriverException as e:
            logger.error(f"Failed to initialize browser driver: {e}")
            raise

    def close(self) -> None:
        """Close the browser and clean up resources."""
        if self._driver:
            try:
                self._driver.quit()
                logger.debug("Browser driver closed")
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
            finally:
                self._driver = None

    def __enter__(self):
        """Context manager entry."""
        return self.get_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
