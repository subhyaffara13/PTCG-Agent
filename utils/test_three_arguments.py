
def test_three_arguments():
    with tm.assert_produces_warning(WARNING_CATEGORY):
        assert f(6, 3, 3) == 12

