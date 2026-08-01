
def test_issue_11463():
    numpy = import_module('numpy')
    if not numpy:
        skip("numpy not installed.")
    x = Symbol('x')
    f = lambdify(x, real_root((log(x/(x-2))), 3), 'numpy')
    # numpy.select evaluates all options before considering conditions,
    # so it raises a warning about root of negative number which does
    # not affect the outcome. This warning is suppressed here
    with ignore_warnings(RuntimeWarning):
        assert f(numpy.array(-1)) < -1

