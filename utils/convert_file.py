import sys

def convert_file(filename: str) -> None:
    """
    Parse a Markdown file and dump the output to stdout.
    """
    try:
        with open(filename, encoding="utf8", errors="ignore") as fin:
            rendered = MarkdownIt().render(fin.read())
            print(rendered, end="")
    except OSError:
        sys.stderr.write(f'Cannot open file "{filename}".\n')
        sys.exit(1)

