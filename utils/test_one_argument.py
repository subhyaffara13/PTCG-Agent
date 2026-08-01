
def test_one_argument():
    with tm.assert_produces_warning(None):
        assert f(19) == 19

