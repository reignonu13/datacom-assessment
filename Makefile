VENV_DIR      ?= playwright-qa
BROWSER       ?= chromium

ifeq ($(OS),Windows_NT)
    PYTHON   ?= python
    VENV_BIN := $(VENV_DIR)/Scripts
    OPEN     := cmd /c start ""
else
    PYTHON   ?= python3
    VENV_BIN := $(VENV_DIR)/bin
    UNAME    := $(shell uname -s)
    ifeq ($(UNAME),Darwin)
        OPEN := open
    else
        OPEN := xdg-open
    endif
endif

VENV_PYTHON   := $(VENV_BIN)/python
PIP           := $(VENV_PYTHON) -m pip
PYTEST        := $(VENV_BIN)/pytest
PLAYWRIGHT    := $(VENV_BIN)/playwright

.DEFAULT_GOAL := help

.PHONY: venv
venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

.PHONY: install
install: venv ## Install pip dependencies
	$(PIP) install -r requirements.txt

.PHONY: install-browsers
install-browsers: ## Download Playwright browser binaries
	$(PLAYWRIGHT) install --with-deps $(BROWSER)

.PHONY: setup
setup: install install-browsers ## Full setup (venv + deps + browsers)
	@$(PYTHON) -c "import sys, os; d='$(VENV_DIR)'; act = os.path.join(d, 'Scripts', 'activate') if sys.platform == 'win32' else 'source ' + d + '/bin/activate'; print('Environment ready. Activate with: ' + act)"

.PHONY: test
test: ## Run test suite headless
	@$(PYTHON) -c "import os; os.makedirs('reports', exist_ok=True)"
	$(PYTEST) tests/ --browser $(BROWSER)

.PHONY: test-headed
test-headed: ## Run tests with visible browser
	@$(PYTHON) -c "import os; os.makedirs('reports', exist_ok=True)"
	$(PYTEST) tests/ --browser $(BROWSER) --headed

.PHONY: test-parallel
test-parallel: ## Run tests across multiple workers
	@$(PYTHON) -c "import os; os.makedirs('reports', exist_ok=True)"
	$(PYTEST) tests/ --browser $(BROWSER) -n auto

.PHONY: report
report: ## Open HTML report in browser
	$(OPEN) reports/report.html

.PHONY: clean
clean: ## Remove generated reports and caches
	@$(PYTHON) -c "import os, glob; [os.remove(f) for f in glob.glob('reports/*.xml') + glob.glob('reports/*.html') if os.path.isfile(f)]"
	@$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]"
	@$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.pytest_cache') if p.is_dir()]"
	@$(PYTHON) -c "import shutil; shutil.rmtree('reports/playwright', ignore_errors=True)"

.PHONY: clean-all
clean-all: clean ## Remove everything including venv
	@$(PYTHON) -c "import shutil; shutil.rmtree('$(VENV_DIR)', ignore_errors=True)"
