
def test_is_partial():
    test_is_valid(check_valid=is_partial_args, incomplete=True)
    test_is_valid_py3(check_valid=is_partial_args, incomplete=True)


def test_is_partial():
    test_is_valid(check_valid=_is_partial_args, incomplete=True)

