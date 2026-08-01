
def assert_target_equivalence(name: str, expected: list[str], actual: list[str]) -> None:
    """Compare actual and expected targets (order sensitive)."""
    assert_string_arrays_equal(
        expected,
        actual,
        ('Actual targets ({}) do not match expected targets ({}) for "[{} ...]"').format(
            ", ".join(actual), ", ".join(expected), name
        ),
    )

