
def test_issue548():
    try:
        # This expression is invalid, but may trigger the ReDOS vulnerability
        # in the regular expression for parsing complex numbers.
        mpmathify('(' + '1' * 5000 + '!j')
    except:
        return
    # The expression is invalid and should raise an exception.
    assert False

