
def assert_module_equivalence(name: str, expected: Iterable[str], actual: Iterable[str]) -> None:
    expected_normalized = sorted(expected)
    actual_normalized = sorted(set(actual).difference({"__main__"}))
    assert_string_arrays_equal(
        expected_normalized,
        actual_normalized,
        ('Actual modules ({}) do not match expected modules ({}) for "[{} ...]"').format(
            ", ".join(actual_normalized), ", ".join(expected_normalized), name
        ),
    )

