
def sympify_return(*args):
    '''Function/method decorator to sympify arguments automatically

    See the docstring of sympify_method_args for explanation.
    '''
    # Store a wrapper object for the decorated method
    def wrapper(func: Callable[[T1, T2], T3]) -> Callable[[T1, T2], T3]:
        return _SympifyWrapper(func, args)  # type: ignore
    return wrapper

