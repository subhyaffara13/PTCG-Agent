
def test_four_arguments():
    with tm.assert_produces_warning(WARNING_CATEGORY):
        assert f(1, 2, 3, 4) == 10

