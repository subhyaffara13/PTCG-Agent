
def _diff_text(
    left: str, right: str, highlighter: _HighlightFunc, verbose: int = 0
) -> Iterator[str]:
    """Yield the explanation for the diff between text.

    Unless --verbose is used this will skip leading and trailing
    characters which are identical to keep the diff minimal.
    """
    from difflib import ndiff

    if verbose < 1:
        i = 0  # just in case left or right has zero length
        for i in range(min(len(left), len(right))):
            if left[i] != right[i]:
                break
        if i > 42:
            i -= 10  # Provide some context
            yield f"Skipping {i} identical leading characters in diff, use -v to show"
            left = left[i:]
            right = right[i:]
        if len(left) == len(right):
            for i in range(len(left)):
                if left[-i] != right[-i]:
                    break
            if i > 42:
                i -= 10  # Provide some context
                yield (
                    f"Skipping {i} identical trailing "
                    "characters in diff, use -v to show"
                )
                left = left[:-i]
                right = right[:-i]
    keepends = True
    if left.isspace() or right.isspace():
        left = repr(str(left))
        right = repr(str(right))
        yield "Strings contain only whitespace, escaping them using repr()"
    # "right" is the expected base against which we compare "left",
    # see https://github.com/pytest-dev/pytest/issues/3333
    yield from highlighter(
        "\n".join(
            line.strip("\n")
            for line in ndiff(right.splitlines(keepends), left.splitlines(keepends))
        ),
        lexer="diff",
    ).splitlines()

