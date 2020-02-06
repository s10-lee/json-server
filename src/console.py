# Console class helper
# write colors into console
# - white doesnt work


class Console:

    schema = {
        'white': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'purple': '35',
        'cyan': '36',
        'gray': '37'
    }

    @classmethod
    def wrap_text(cls, text, color=None, bold=False):
        # color_code = cls.schema.get(color, '37')
        # prefix = int(bold)
        return f"\033[{int(bold)};{cls.schema.get(color, '37')}m{text}\033[0m"

    @classmethod
    def write(cls, text, color=None, bold=False):
        print(cls.wrap_text(text, color, bold))
