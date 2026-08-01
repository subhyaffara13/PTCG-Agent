
def test_one_and_one_arguments():
    with tm.assert_produces_warning(None):
        assert f(19, d=6) == 25

