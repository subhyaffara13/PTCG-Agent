
def array_ufunc_errmsg_formatter(dummy, ufunc, method, *inputs, **kwargs):
    """ Format the error message for when __array_ufunc__ gives up. """
    args_string = ', '.join([f'{arg!r}' for arg in inputs] +
                            [f'{k}={v!r}'
                             for k, v in kwargs.items()])
    args = inputs + kwargs.get('out', ())
    types_string = ', '.join(repr(type(arg).__name__) for arg in args)
    return ('operand type(s) all returned NotImplemented from '
            f'__array_ufunc__({ufunc!r}, {method!r}, {args_string}): {types_string}'
            )

