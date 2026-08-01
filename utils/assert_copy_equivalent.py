
def assert_copy_equivalent(operation, args, out, **kwargs):
    """
    Check that operation(*args, out=out) produces results
    equivalent to out[...] = operation(*args, out=out.copy())
    """

    kwargs['out'] = out
    kwargs2 = dict(kwargs)
    kwargs2['out'] = out.copy()

    out_orig = out.copy()
    out[...] = operation(*args, **kwargs2)
    expected = out.copy()
    out[...] = out_orig

    got = operation(*args, **kwargs).copy()

    if (got != expected).any():
        assert_equal(got, expected)

