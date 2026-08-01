
def _diff(expected: str, actual: str) -> str:
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="old_prompt",
            tofile="new_prompt",
            n=2,
        )
    )


def _diff(expected: str, actual: str) -> str:
    """Return a unified diff between two strings."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="old_prompt",
            tofile="new_prompt",
            n=2,
        )
    )


def _diff(expected: str, actual: str) -> str:
    """Return a unified diff between two strings."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="old_prompt",
            tofile="new_prompt",
            n=2,
        )
    )

