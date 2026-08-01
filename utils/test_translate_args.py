
def test_translate_args():
    try:
        translate(None, None, None, 'not_none')
    except ValueError:
        pass # Exception raised successfully
    else:
        assert False

    assert translate('s', None, None, None) == 's'

    try:
        translate('s', 'a', 'bc')
    except ValueError:
        pass # Exception raised successfully
    else:
        assert False

