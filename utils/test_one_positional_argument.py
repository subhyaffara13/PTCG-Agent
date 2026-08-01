
def test_one_positional_argument():
    with tm.assert_produces_warning(WARNING_CATEGORY):
        assert h(23) == 23

