import sys

def capture_output() -> Generator[StringIO, None, None]:
    """Capture output that is printed to terminal.

    Taken from https://stackoverflow.com/a/34738440

    Example:
    ```py
    >>> with capture_output() as output:
    ...     print("hello world")
    >>> assert output.getvalue() == "hello world\n"
    ```
    """
    output = StringIO()
    previous_output = sys.stdout
    sys.stdout = output
    try:
        yield output
    finally:
        sys.stdout = previous_output

