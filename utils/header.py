
def header(text, style='-'):
    return text + '\n' + style*len(text) + '\n'


def header(text, *args):
    return f"{COLOR['HEADER']}{text % args}{COLOR['DEFAULT']}"

