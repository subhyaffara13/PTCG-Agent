
def convert_stdin() -> None:
    """
    Parse a Markdown file and dump the output to stdout.
    """
    try:
        rendered = MarkdownIt().render(sys.stdin.read())
        print(rendered, end="")
    except OSError:
        sys.stderr.write("Cannot parse Markdown from the standard input.\n")
        sys.exit(1)

