import pytest
from playwright.sync_api import Page

from config.settings import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, DEFAULT_TIMEOUT
from pages.bugs_form_page import BugsFormPage


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        'viewport': {'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT},
    }


@pytest.fixture(scope='function')
def bugs_form(page: Page) -> BugsFormPage:
    page.set_default_timeout(DEFAULT_TIMEOUT)
    form = BugsFormPage(page)
    form.open()
    return form
