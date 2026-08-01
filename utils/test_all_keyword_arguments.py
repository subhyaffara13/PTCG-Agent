
def test_all_keyword_arguments():
    with tm.assert_produces_warning(None):
        assert h(a=1, b=2) == 3

