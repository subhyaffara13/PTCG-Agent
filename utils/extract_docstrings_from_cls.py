
def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]:
    """Map model attributes and their corresponding docstring.

    Args:
        cls: The class of the Pydantic model to inspect.
        use_inspect: Whether to skip usage of frames to find the object and use
            the `inspect` module instead.

    Returns:
        A mapping containing attribute names and their corresponding docstring.
    """
    if use_inspect or sys.version_info >= (3, 13):
        # On Python < 3.13, `inspect.getsourcelines()` might not work as expected
        # if two classes have the same name in the same source file.
        # On Python 3.13+, it will use the new `__firstlineno__` class attribute,
        # making it way more robust.
        try:
            source, _ = inspect.getsourcelines(cls)
        except OSError:  # pragma: no cover
            return {}
    else:
        # TODO remove this implementation when we drop support for Python 3.12:
        source = _extract_source_from_frame(cls)

    if not source:
        return {}

    dedent_source = _dedent_source_lines(source)

    visitor = DocstringVisitor()
    visitor.visit(ast.parse(dedent_source))
    return visitor.attrs

