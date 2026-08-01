
def test_map_arg_as_kwarg():
    with tm.assert_produces_warning(
        Pandas4Warning, match="`arg` has been renamed to `func`"
    ):
        Series([1, 2]).map(arg={})

