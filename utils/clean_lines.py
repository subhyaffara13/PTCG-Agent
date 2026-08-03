import pathlib

def clean_lines(filepath):
    with pathlib.Path(filepath).open(encoding='utf-8') as f:
        yield from filter(None, map(str.strip, f))

