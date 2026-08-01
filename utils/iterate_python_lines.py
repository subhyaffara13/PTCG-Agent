
def iterate_python_lines(path: str) -> Iterator[tuple[int, str]]:
    """Return an iterator over (line number, line text) from a Python file."""
    if not os.path.isdir(path):  # can happen with namespace packages
        with tokenize.open(path) as input_file:
            yield from enumerate(input_file, 1)

