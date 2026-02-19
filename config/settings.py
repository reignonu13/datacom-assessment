import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'https://qa-practice.netlify.app')
BUGS_FORM_PATH = '/bugs-form'
BUGS_FORM_URL = f'{BASE_URL}{BUGS_FORM_PATH}'

DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10000'))
VIEWPORT_WIDTH = int(os.getenv('VIEWPORT_WIDTH', '1366'))
VIEWPORT_HEIGHT = int(os.getenv('VIEWPORT_HEIGHT', '768'))
