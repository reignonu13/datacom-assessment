# Datacom Coding Exam - AI Quality Assurance Lead

Assessment completed by Jay Sisley to test https://qa-practice.netlify.app/bugs-form using Playwright and Python where:

- The test case will give value if automated
- The test can be developed in the allocated 4 hr
- Be prepared to show and discuss code and testing approach
- *Optional:* to run via CI pipeline.
- *Optional:* Expand on the original scope

## Prerequisites

| Requirement | Minimum version |
|-------------|-----------------|
| Python      | 3.11            |
| make        | any             |

## Setup

Creates venv, installs pip deps, installs Playwright browsers.

### Using Make

```bash
make setup
```

### Manually via Windows

```powershell
python -m venv playwright-qa
.\playwright-qa\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install --with-deps chromium
```

### Manually via Linux/macOS

```bash
python3 -m venv playwright-qa
source playwright-qa/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium
```

## Running Tests

```bash
make test          # full suite (headless)
make test-headed   # full suite with visible browser
make test-parallel # full suite across multiple workers
make report        # open HTML report in browser
make clean         # remove generated reports and caches
```

Override browser at run-time:

```bash
BROWSER=firefox make test
BROWSER=webkit  make test-headed
```

### Reports

After each run two reports are written to `reports/`:

- `junit-results.xml` — consumed by CI systems (Azure DevOps, Jenkins, etc.)
- `report.html` — self-contained HTML report

## Test Data

Tests are data-driven from two JSON files:

| File                         | Purpose                                                         |
|------------------------------|-----------------------------------------------------------------|
| `test_data/page_state.json`  | Page state checks: labels, field types, hints, dropdown options |
| `test_data/scenarios.json`   | Form submissions: defaults, happy paths, validation, edge cases |

Each scenario in `scenarios.json` only overrides the fields it needs to test — everything else falls back to a shared `defaults` block so the data stays readable.

## Bugs

The tests are written to describe *expected* behaviour. Any test failure points to a bug on the page. The table below maps what I found during manual exploration and then confirmed with automated checks.

| Bug    | Scenario IDs                              | Summary                                           |
|--------|-------------------------------------------|---------------------------------------------------|
| BUG-01 | `BugForm_01`, `BugForm_33`                | First Name label missing asterisk, empty accepted |
| BUG-02 | `BugForm_35`, `BugForm_54`                | Last Name empty accepted, display truncates last char |
| BUG-03 | `BugForm_37`, `BugForm_38`                | Phone accepts non-numeric, hint wording is wrong  |
| BUG-04 | `BugForm_31`, `BugForm_32`                | Phone last digit incremented on display           |
| BUG-05 | `BugForm_13`, `BugForm_39`                | Country placeholder not disabled, can be submitted |
| BUG-06 | `BugForm_07`, `BugForm_40`..`42`          | Email input type="text" instead of "email"        |
| BUG-07 | `BugForm_08`                              | Password input type="text", value visible on screen |
| BUG-08 | `BugForm_47`, `BugForm_26`                | 20-char password rejected (off-by-one in validation) |
| BUG-09 | `BugForm_49`                              | Form submits without T&C checkbox checked         |
| BUG-10 | `BugForm_10`                              | T&C label has no hyperlink                        |
| BUG-11 | `BugForm_03`, `BugForm_23`, `60`..`62`    | Label typo "nunber"; phone/country/email/password labels' `for` attribute targets wrong element |
| BUG-12 | `BugForm_09`                              | Hint abbreviates "Password" as "Psw"              |
| BUG-13 | `BugForm_12`                              | "mandatory" note sits under Last Name, not at top |
| BUG-14 | `BugForm_14`..`22`                        | Dropdown: 6 value typos + 3 display-name typos   |
| BUG-15 | `BugForm_51`, `BugForm_52`                | Submitting all-empty only reports password error  |
|        | `BugForm_55`                              | Success banner uses `alert-danger` CSS class      |
|        | `BugForm_11`                              | T&C checkbox is disabled in the DOM               |
|        | `BugForm_57`                              | Password stored in plaintext in localStorage      |

### Approach and trade-offs

- I went with a data-driven pattern (JSON files + parametrize) because this form has many fields and the same assertion logic repeats across scenarios. It keeps the test file short while still giving each case its own name in the report.
- The T&C checkbox is disabled in the DOM, so the page object uses a JS workaround (`el.checked = true`) to unblock submission tests for the other fields. The disabled state itself is tested separately in `BugForm_11`.
- If I had more time I'd add keyboard/tab-order tests and possibly check that the form works at different viewport sizes.
