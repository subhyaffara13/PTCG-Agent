
def DEBUG_WRAP(func):
    def wrap(*args, **kwargs):
        from sympy import SYMPY_DEBUG
        global _LT_level

        if not SYMPY_DEBUG:
            return func(*args, **kwargs)

        if _LT_level == 0:
            print('\n' + '-'*78, file=sys.stderr)
        print('-LT- %s%s%s' % ('  '*_LT_level, func.__name__, args),
              file=sys.stderr)
        _LT_level += 1
        if (
                func.__name__ == '_laplace_transform_integration' or
                func.__name__ == '_inverse_laplace_transform_integration'):
            sympy.SYMPY_DEBUG = False
            print('**** %sIntegrating ...' % ('  '*_LT_level), file=sys.stderr)
            result = func(*args, **kwargs)
            sympy.SYMPY_DEBUG = True
        else:
            result = func(*args, **kwargs)
        _LT_level -= 1
        print('-LT- %s---> %s' % ('  '*_LT_level, result), file=sys.stderr)
        if _LT_level == 0:
            print('-'*78 + '\n', file=sys.stderr)
        return result
    return wrap

