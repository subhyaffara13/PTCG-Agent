import functools

def test_is_valid(check_valid=is_valid_args, incomplete=False):
    orig_check_valid = check_valid
    check_valid = lambda func, *args, **kwargs: orig_check_valid(func, args, kwargs)

    f = make_func('')
    assert check_valid(f)
    assert check_valid(f, 1) is False
    assert check_valid(f, x=1) is False

    f = make_func('x')
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, x=1)
    assert check_valid(f, 1, x=2) is False
    assert check_valid(f, 1, y=2) is False
    assert check_valid(f, 1, 2) is False
    assert check_valid(f, x=1, y=2) is False

    f = make_func('x=1')
    assert check_valid(f)
    assert check_valid(f, 1)
    assert check_valid(f, x=1)
    assert check_valid(f, 1, x=2) is False
    assert check_valid(f, 1, y=2) is False
    assert check_valid(f, 1, 2) is False
    assert check_valid(f, x=1, y=2) is False

    f = make_func('*args')
    assert check_valid(f)
    assert check_valid(f, 1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, x=1) is False

    f = make_func('**kwargs')
    assert check_valid(f)
    assert check_valid(f, x=1)
    assert check_valid(f, x=1, y=2)
    assert check_valid(f, 1) is False

    f = make_func('x, *args')
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, x=1)
    assert check_valid(f, 1, x=1) is False
    assert check_valid(f, 1, y=1) is False

    f = make_func('x, y=1, **kwargs')
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, x=1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, x=1, y=2, z=3)
    assert check_valid(f, 1, 2, y=3) is False

    f = make_func('a, b, c=3, d=4')
    assert check_valid(f) is incomplete
    assert check_valid(f, 1) is incomplete
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, c=3) is incomplete
    assert check_valid(f, 1, e=3) is False
    assert check_valid(f, 1, 2, e=3) is False
    assert check_valid(f, 1, 2, b=3) is False

    assert check_valid(1) is False


def test_is_valid(check_valid=_is_valid_args, incomplete=False):
    orig_check_valid = check_valid
    check_valid = lambda func, *args, **kwargs: orig_check_valid(func, args, kwargs)

    assert check_valid(lambda x: None) is None

    f = builtins.abs
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, x=1) is False
    assert check_valid(f, 1, 2) is False

    f = builtins.complex
    assert check_valid(f)
    assert check_valid(f, 1)
    assert check_valid(f, real=1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, imag=2)
    assert check_valid(f, 1, real=2) is False
    assert check_valid(f, 1, 2, 3) is False
    assert check_valid(f, 1, 2, imag=3) is False

    f = builtins.int
    assert check_valid(f)
    assert check_valid(f, 1)
    assert check_valid(f, x=1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, base=2)
    assert check_valid(f, x=1, base=2)
    assert check_valid(f, base=2) is incomplete
    assert check_valid(f, 1, 2, 3) is False

    f = builtins.map
    assert check_valid(f) is incomplete
    assert check_valid(f, 1) is incomplete
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, 2, 3)
    assert check_valid(f, 1, 2, 3, 4)

    f = builtins.min
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, iterable=1) is False
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, 2, 3)
    assert check_valid(f, key=None) is incomplete
    assert check_valid(f, 1, key=None)
    assert check_valid(f, 1, 2, key=None)
    assert check_valid(f, 1, 2, 3, key=None)
    assert check_valid(f, key=None, default=None) is incomplete
    assert check_valid(f, 1, key=None, default=None)
    assert check_valid(f, 1, 2, key=None, default=None) is False
    assert check_valid(f, 1, 2, 3, key=None, default=None) is False

    f = builtins.range
    assert check_valid(f) is incomplete
    assert check_valid(f, 1)
    assert check_valid(f, 1, 2)
    assert check_valid(f, 1, 2, 3)
    assert check_valid(f, 1, 2, step=3) is False
    assert check_valid(f, 1, 2, 3, 4) is False

    f = functools.partial
    assert orig_check_valid(f, (), {}) is incomplete
    assert orig_check_valid(f, (), {'func': 1}) is incomplete
    assert orig_check_valid(f, (1,), {})
    assert orig_check_valid(f, (1,), {'func': 1})
    assert orig_check_valid(f, (1, 2), {})

