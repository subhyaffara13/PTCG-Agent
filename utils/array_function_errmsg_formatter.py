
def array_function_errmsg_formatter(public_api, types):
    """ Format the error message for when __array_ufunc__ gives up. """
    func_name = f'{public_api.__module__}.{public_api.__name__}'
    return (f"no implementation found for '{func_name}' on types that implement "
            f'__array_function__: {list(types)}')

