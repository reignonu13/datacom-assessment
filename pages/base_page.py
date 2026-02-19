import logging
from playwright.sync_api import Page
from config.settings import DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page
        self.timeout = DEFAULT_TIMEOUT

    def navigate(self, url: str) -> None:
        logger.info('Navigating to %s', url)
        self.page.goto(url, wait_until='networkidle', timeout=self.timeout)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click(timeout=self.timeout)

    def double_click(self, selector: str) -> None:
        self.page.locator(selector).dblclick(timeout=self.timeout)

    def clear_and_fill(self, selector: str, value: str) -> None:
        locator = self.page.locator(selector)
        locator.clear(timeout=self.timeout)
        locator.fill(value, timeout=self.timeout)

    def select_option(self, selector: str, value: str) -> None:
        # label= matches the visible text, which is what a real user sees
        self.page.locator(selector).select_option(label=value, timeout=self.timeout)

    def force_check_checkbox(self, selector: str) -> None:
        # the T&C checkbox is disabled in the DOM (that's a separate bug we test for),
        # so we set checked via JS to unblock submission tests for other fields
        self.page.locator(selector).evaluate('el => el.checked = true')

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text(timeout=self.timeout)

    def get_attribute(self, selector: str, attribute: str) -> str | None:
        return self.page.locator(selector).get_attribute(attribute, timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        return self.page.locator(selector).is_enabled()

    def reload(self) -> None:
        self.page.reload(wait_until='networkidle', timeout=self.timeout)

    def wait_for_selector(self, selector: str, state: str = 'visible') -> None:
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)

    def get_local_storage_item(self, key: str) -> str | None:
        return self.page.evaluate('(key) => localStorage.getItem(key)', key)

    def get_input_type(self, selector: str) -> str:
        return self.get_attribute(selector, 'type') or ''

    def get_element_classes(self, selector: str) -> list[str]:
        raw = self.get_attribute(selector, 'class')
        return raw.split() if raw else []
