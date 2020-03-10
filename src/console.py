from src.settings import CRLF

#   Main Styles
#       3x - Text Color
#       4x - Background
#       5x -
#   Additional:
#       1 = Bold
#       2 = Transparent Text
#       3 = Italic
#       4 = Underline
#       5 = Blink
#       6 - Normal Font
#       7 - Invert Text Color
#       8 = No Text


def parse_line(text: str):
    for color, code in {'red': 1, 'green': 2, 'yellow': 3, 'cyan': 6, 'gray': 7, 'white': 8}.items():
        text = text.replace(f'<{color}>', f"\033[1;3{code}m").replace(f'</{color}>', '\033[0m')
    text = text.replace('<nl>', CRLF)
    return text


def print_line(*args, sep=''):
    text = sep.join(args)
    print(parse_line(text))


def color_text(text, color, bold='1'):
    return f"\033[{bold};{color}m{text}\033[0m"
