
def test_curry_module():
    from toolz.curried.exceptions import merge
    assert merge.__module__ == 'toolz.curried.exceptions'

