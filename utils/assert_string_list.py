
def assert_string_list(dist, attr: str, value: _Sequence) -> None:
    """Verify that value is a string list"""
    try:
        # verify that value is a list or tuple to exclude unordered
        # or single-use iterables
        assert isinstance(value, _sequence)
        # verify that elements of value are strings
        assert ''.join(value) != value
    except (TypeError, ValueError, AttributeError, AssertionError) as e:
        raise DistutilsSetupError(
            f"{attr!r} must be of type <{_sequence_type_repr}> (got {value!r})"
        ) from e

