import json
import pytest
from pathlib import Path

from pages.bugs_form_page import BugsFormPage

TEST_DATA = Path(__file__).parent.parent / 'test_data'


def load_json(filename: str):
    with open(TEST_DATA / filename, encoding='utf-8') as fh:
        return json.load(fh)


_page = load_json('page_state.json')
_scenarios = load_json('scenarios.json')

DEFAULTS = _scenarios['defaults']
FORM_KEYS = ('first_name', 'last_name', 'phone', 'country', 'email', 'password', 'check_terms')


def _merge(scenario):
    # each scenario only overrides the fields it cares about; everything else
    # falls back to DEFAULTS so we're not repeating valid data in every row
    return {k: scenario[k] if k in scenario else DEFAULTS.get(k) for k in FORM_KEYS}


def _make_params(items, id_key='id'):
    return [pytest.param(item, id=str(item[id_key])) for item in items]


def _check_page(form, c):
    t = c['type']
    if t == 'label':
        return form.get_label_text(c['input_id'])
    if t == 'label_for':
        return form.get_label_for_attr(c['input_id'])
    if t == 'field_type':
        return form.get_input_type('#' + c['input_id'])
    if t == 'hint':
        return form.get_hint_text(c['input_id'])
    if t == 'tc_link':
        return form.has_link_near(c['input_id'])
    if t == 'tc_enabled':
        return form.is_enabled('#' + c['input_id'])
    if t == 'note_position':
        return form.get_mandatory_note_position()
    if t == 'placeholder_disabled':
        return form.is_first_option_disabled(c['input_id'])
    if t == 'option_value':
        return form.get_country_option_value(c['display'])
    if t == 'display_name':
        return c['search'] in form.get_country_option_texts()


@pytest.mark.parametrize('check', _make_params(_page))
def test_page_state(bugs_form: BugsFormPage, check: dict):
    """Verify the form's static structure matches what an end user would expect.
    Failures here mean the page itself is wrong before anyone touches a field."""
    actual = _check_page(bugs_form, check)
    assert actual == check['expected'], f"{check['id']}: expected {check['expected']!r}, got {actual!r}"


@pytest.mark.parametrize('sc', _make_params(_scenarios['submissions']))
def test_submission(bugs_form: BugsFormPage, sc: dict):
    merged = _merge(sc)
    bugs_form.fill_and_submit(**merged)
    bugs_form.assert_results_visible()
    msg = bugs_form.get_text('#message')

    if sc['expected_state'] == 'success':
        assert 'Successfully registered' in msg, f"Expected success but got: {msg}"
        for field, expected in sc.get('expected_output', {}).items():
            bugs_form.assert_result(field, expected)
        if 'expected_css_class' in sc:
            bugs_form.assert_message_css_class_contains(sc['expected_css_class'])
        if sc.get('check_password_hidden'):
            bugs_form.assert_password_not_in_results(merged['password'])
        if sc.get('check_no_localstorage'):
            bugs_form.assert_password_not_in_local_storage(merged['email'])
    else:
        assert sc['expected_message'] in msg, f"Expected '{sc['expected_message']}' in: {msg}"

    # optional post-submission checks
    if sc.get('then_refresh'):
        bugs_form.reload()
        bugs_form.assert_results_hidden()
    if sc.get('then_double_click'):
        bugs_form.double_click_register()
        bugs_form.assert_results_hidden()

    # TODO: could add tab-order / keyboard-nav tests if time allows
