from src.settings import SCHEMA


def color_text(text, color, bold=True):
    return f"\033[{int(bold)};{SCHEMA.get(color, '37')}m{text}\033[0m"


def red(text):
    return f"\033[1;31m{text}\033[0m"


def green(text):
    return f"\033[1;32m{text}\033[0m"


def cyan(text):
    return f"\033[1;36m{text}\033[0m"


def yellow(text):
    return f"\033[1;33m{text}\033[0m"
