
def _workers_wrapper(func):
    """
    Wrapper to deal with setup-cleanup of workers outside a user function via a
    ContextManager. It saves having to do the setup/tear down with within that
    function, which can be messy.
    """
    @functools.wraps(func)
    def inner(*args, **kwds):
        kwargs = kwds.copy()
        if 'workers' not in kwargs:
            _workers = map
        elif 'workers' in kwargs and kwargs['workers'] is None:
            _workers = map
        else:
            _workers = kwargs['workers']

        with MapWrapper(_workers) as mf:
            kwargs['workers'] = mf
            return func(*args, **kwargs)

    return inner

