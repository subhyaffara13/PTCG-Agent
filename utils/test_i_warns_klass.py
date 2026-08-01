
def test_i_warns_klass():
    with tm.assert_produces_warning(WARNING_CATEGORY):
        assert i(1, 2) == 3

