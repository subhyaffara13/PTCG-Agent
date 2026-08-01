
def _compare_eq_iterable(
    left: Iterable[object],
    right: Iterable[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
) -> Iterator[str]:
    if verbose <= 0 and not running_on_ci():
        yield "Use -v to get more diff"
        return
    # dynamic import to speedup pytest
    import difflib

    left_formatting = PrettyPrinter().pformat(left).splitlines()
    right_formatting = PrettyPrinter().pformat(right).splitlines()

    yield ""
    yield "Full diff:"
    # "right" is the expected base against which we compare "left",
    # see https://github.com/pytest-dev/pytest/issues/3333
    yield from highlighter(
        "\n".join(
            line.rstrip() for line in difflib.ndiff(right_formatting, left_formatting)
        ),
        lexer="diff",
    ).splitlines()

