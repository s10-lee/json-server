from src.settings import SCHEMA, CRLF


def parse_line(text):
    for color, code in {'white': 0,'red': 1, 'green': 2, 'yellow': 3, 'cyan': 6, 'gray': 7}.items():
        text = text.replace(f'<{color}>', f"\033[1;3{code}m").replace(f'</{color}>', '\033[0m')
    text = text.replace('<nl>', CRLF)
    return text


def print_line(text):
    print(parse_line(text))


# def color_text(text, color, bold=True):
#     return f"\033[{int(bold)};{SCHEMA.get(color, '37')}m{text}\033[0m"
