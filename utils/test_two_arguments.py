
def test_two_arguments():
    with tm.assert_produces_warning(None):
        assert f(1, 5) == 6

