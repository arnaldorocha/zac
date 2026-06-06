"""
Browser automation service using Playwright.
"""
import logging
from typing import Optional, List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class BrowserAutomationService:
    """Handles browser automation using Playwright."""
    
    def __init__(self, headless: bool = False, browser_type: str = "chromium"):
        """
        Initialize browser service.
        
        Args:
            headless: Run browser in headless mode
            browser_type: Type of browser ('chromium', 'firefox', 'webkit')
        """
        self.headless = headless
        self.browser_type = browser_type
        self.browser = None
        self.page = None
        self.context = None
    
    def _get_browser_module(self):
        """Get the appropriate Playwright browser module."""
        try:
            from playwright.sync_api import sync_playwright
            return sync_playwright()
        except ImportError:
            logger.error("Playwright not installed. Install with: pip install playwright")
            raise
    
    def open_browser(self, url: Optional[str] = None) -> bool:
        """
        Open browser window.
        
        Args:
            url: Initial URL to navigate to
            
        Returns:
            True if successful
        """
        try:
            if self.browser:
                logger.warning("Browser already open")
                return True
            
            p = self._get_browser_module()
            self.browser = p.start()
            
            # Select browser type
            if self.browser_type == "firefox":
                browser_instance = self.browser.firefox.launch(headless=self.headless)
            elif self.browser_type == "webkit":
                browser_instance = self.browser.webkit.launch(headless=self.headless)
            else:
                browser_instance = self.browser.chromium.launch(headless=self.headless)
            
            self.context = browser_instance.new_context()
            self.page = self.context.new_page()
            
            if url:
                self.page.goto(url)
            
            logger.info(f"Browser opened ({self.browser_type})")
            return True
            
        except Exception as e:
            logger.error(f"Error opening browser: {e}")
            return False
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            logger.info(f"Navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return False
    
    def click(self, selector: str) -> bool:
        """Click element by selector."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.click(selector)
            logger.info(f"Clicked element: {selector}")
            return True
        except Exception as e:
            logger.error(f"Error clicking {selector}: {e}")
            return False
    
    def fill(self, selector: str, text: str) -> bool:
        """Fill input field."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.fill(selector, text)
            logger.info(f"Filled {selector} with text")
            return True
        except Exception as e:
            logger.error(f"Error filling {selector}: {e}")
            return False
    
    def type_text(self, selector: str, text: str, delay: int = 50) -> bool:
        """Type text with delay (simulating manual typing)."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.type(selector, text, delay=delay)
            logger.info(f"Typed text in {selector}")
            return True
        except Exception as e:
            logger.error(f"Error typing in {selector}: {e}")
            return False
    
    def get_text(self, selector: str) -> Optional[str]:
        """Get text content of element."""
        if not self.page:
            logger.error("Browser not open")
            return None
        
        try:
            text = self.page.text_content(selector)
            return text
        except Exception as e:
            logger.error(f"Error getting text from {selector}: {e}")
            return None
    
    def get_all_text(self, selector: str) -> List[str]:
        """Get text from all matching elements."""
        if not self.page:
            logger.error("Browser not open")
            return []
        
        try:
            elements = self.page.query_selector_all(selector)
            texts = [elem.text_content() for elem in elements]
            return texts
        except Exception as e:
            logger.error(f"Error getting texts from {selector}: {e}")
            return []
    
    def element_exists(self, selector: str) -> bool:
        """Check if element exists."""
        if not self.page:
            return False
        
        try:
            return self.page.query_selector(selector) is not None
        except:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = 5000) -> bool:
        """Wait for element to appear."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Element {selector} not found within timeout: {e}")
            return False
    
    def take_screenshot(self, path: str) -> bool:
        """Take screenshot."""
        if not self.page:
            logger.error("Browser not open")
            return False
        
        try:
            self.page.screenshot(path=path)
            logger.info(f"Screenshot saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False
    
    def execute_script(self, script: str) -> Any:
        """Execute JavaScript."""
        if not self.page:
            logger.error("Browser not open")
            return None
        
        try:
            result = self.page.evaluate(script)
            return result
        except Exception as e:
            logger.error(f"Error executing script: {e}")
            return None
    
    def get_page_title(self) -> Optional[str]:
        """Get page title."""
        if not self.page:
            return None
        
        try:
            return self.page.title()
        except:
            return None
    
    def get_page_url(self) -> Optional[str]:
        """Get current page URL."""
        if not self.page:
            return None
        
        try:
            return self.page.url
        except:
            return None
    
    def close_browser(self) -> None:
        """Close browser."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.open_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()
