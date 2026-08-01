
def test_global_cache():
    """ Test use of the global cache. """
    from sympy.printing.aesaracode import global_cache

    backup = dict(global_cache)
    try:
        # Temporarily empty global cache
        global_cache.clear()

        for s in [x, X, f_t]:
            with warns_deprecated_sympy():
                st = aesara_code(s)
                assert aesara_code(s) is st

    finally:
        # Restore global cache
        global_cache.update(backup)


def test_global_cache():
    """ Test use of the global cache. """
    from sympy.printing.theanocode import global_cache

    backup = dict(global_cache)
    try:
        # Temporarily empty global cache
        global_cache.clear()

        for s in [x, X, f_t]:
            with warns_deprecated_sympy():
                st = theano_code(s)
                assert theano_code(s) is st

    finally:
        # Restore global cache
        global_cache.update(backup)

