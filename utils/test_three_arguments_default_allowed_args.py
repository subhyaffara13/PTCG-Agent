
def test_three_arguments_default_allowed_args():
    with tm.assert_produces_warning(WARNING_CATEGORY):
        assert g(6, 3, 3) == 12

