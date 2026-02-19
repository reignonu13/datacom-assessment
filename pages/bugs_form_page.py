from pages.base_page import BasePage
from config.settings import BUGS_FORM_URL


class BugsFormPage(BasePage):

    URL = BUGS_FORM_URL

    RESULTS = {
        'first_name': ('#resultFn', 'First Name'),
        'last_name': ('#resultLn', 'Last Name'),
        'phone': ('#resultPhone', 'Phone Number'),
        'country': ('#country', 'Country'),
        'email': ('#resultEmail', 'Email'),
    }

    def open(self):
        self.navigate(self.URL)

    def fill_form(self, first_name=None, last_name=None, phone=None,
                  country=None, email=None, password=None, check_terms=False):
        if first_name is not None:
            self.clear_and_fill('#firstName', first_name)
        if last_name is not None:
            self.clear_and_fill('#lastName', last_name)
        if phone is not None:
            self.clear_and_fill('#phone', phone)
        if country is not None:
            self.select_option('#countries_dropdown_menu', country)
        if email is not None:
            self.clear_and_fill('#emailAddress', email)
        if password is not None:
            self.clear_and_fill('#password', password)
        if check_terms:
            self.force_check_checkbox('#exampleCheck1')

    def submit(self):
        self.click('#registerBtn')

    def fill_and_submit(self, **kwargs):
        self.fill_form(**kwargs)
        self.submit()

    def double_click_register(self):
        self.double_click('#registerBtn')

    def get_label_text(self, input_id):
        return self.page.evaluate(
            '(id) => document.getElementById(id).closest(".form-group")'
            '.querySelector("label").textContent.trim()',
            input_id,
        )

    def get_label_for_attr(self, input_id):
        return self.page.evaluate(
            '(id) => document.getElementById(id).closest(".form-group")'
            '.querySelector("label").getAttribute("for")',
            input_id,
        )

    def get_hint_text(self, input_id):
        return self.page.evaluate(
            '(id) => document.getElementById(id).closest(".form-group")'
            '.querySelector("small, .form-text").textContent.trim()',
            input_id,
        )

    def has_link_near(self, input_id):
        return self.page.evaluate(
            '(id) => document.getElementById(id)'
            '.closest(".form-group, .form-check")'
            '.querySelector("a") !== null',
            input_id,
        )

    def is_first_option_disabled(self, input_id):
        return self.page.locator('#' + input_id).evaluate(
            '(select) => select.options[0].disabled'
        )

    def get_mandatory_note_position(self):
        return self.page.evaluate("""(() => {
            const groups = document.querySelectorAll('.form-group');
            for (let i = 0; i < groups.length; i++) {
                if (groups[i].textContent.includes('mandatory')) return i;
            }
            return -1;
        })()""")

    def get_country_option_value(self, display_text):
        return self.page.locator('#countries_dropdown_menu').evaluate(
            '(select, text) => { '
            'const opt = Array.from(select.options).find(o => o.text.trim() === text); '
            'return opt ? opt.value : null; '
            '}',
            display_text,
        )

    def get_country_option_texts(self):
        return self.page.locator('#countries_dropdown_menu').evaluate(
            '(select) => Array.from(select.options).map(o => o.text.trim())'
        )

    def assert_result(self, field, expected):
        selector, label = self.RESULTS[field]
        actual = self.get_text(selector)
        assert f'{label}: {expected}' in actual

    def assert_results_visible(self):
        self.wait_for_selector('#results-section', state='visible')

    def assert_results_hidden(self):
        assert not self.is_visible('#results-section')

    def assert_message_css_class_contains(self, css_class):
        classes = self.get_element_classes('#message')
        assert css_class in classes, f"Expected '{css_class}' in {classes}"

    def assert_password_not_in_results(self, password):
        text = self.get_text('#results-section')
        assert password not in text, f"Password visible in results section"

    def assert_password_not_in_local_storage(self, email):
        stored = self.get_local_storage_item(email)
        assert stored is None, f"Password leaked to localStorage['{email}']: '{stored}'"
