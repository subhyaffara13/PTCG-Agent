
def test_errstate():
    for category, error_code in _sf_error_code_map.items():
        for action in _sf_error_actions:
            olderr = sc.geterr()
            with sc.errstate(**{category: action}):
                _check_action(_sf_error_test_function, (error_code,), action)
            assert_equal(olderr, sc.geterr())

