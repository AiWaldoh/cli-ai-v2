import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SSH_HOST = os.environ.get('SSH_HOST', 'localhost')
    SSH_PORT = int(os.environ.get('SSH_PORT', 22))
    SSH_USERNAME = os.environ.get('SSH_USERNAME', '')

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

    WHITELISTED_COMMANDS = ['ls', 'pwd', 'whoami']

    # Define ANSI colors
    ANSI_COLOR_RED = '\033[31m'
    ANSI_COLOR_GREEN = '\033[32m'
    ANSI_COLOR_YELLOW = '\033[33m'
    ANSI_COLOR_BLUE = '\033[34m'
    ANSI_COLOR_MAGENTA = '\033[35m'
    ANSI_COLOR_CYAN = '\033[36m'
    ANSI_COLOR_WHITE = '\033[37m'
    RESET_COLOR = '\033[0m'  # Reset color