
def _call_super_mom(fun):
    # If fit method is overridden only for MLE and doesn't specify what to do
    # if method == 'mm' or with censored data, this decorator calls the generic
    # implementation.
    @wraps(fun)
    def wrapper(self, data, *args, **kwds):
        method = kwds.get('method', 'mle').lower()
        censored = isinstance(data, CensoredData)
        if method == 'mm' or (censored and data.num_censored() > 0):
            return super(type(self), self).fit(data, *args, **kwds)
        else:
            if censored:
                # data is an instance of CensoredData, but actually holds
                # no censored values, so replace it with the array of
                # uncensored values.
                data = data._uncensored
            return fun(self, data, *args, **kwds)

    return wrapper

