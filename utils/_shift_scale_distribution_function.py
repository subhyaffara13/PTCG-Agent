
def _shift_scale_distribution_function(func):
    # c is for complementary
    citem = {'_logcdf_dispatch': '_logccdf_dispatch',
             '_cdf_dispatch': '_ccdf_dispatch',
             '_logccdf_dispatch': '_logcdf_dispatch',
             '_ccdf_dispatch': '_cdf_dispatch'}
    def wrapped(self, x, *args, loc, scale, sign, **kwargs):
        item = func.__name__

        f = getattr(self._dist, item)
        cf = getattr(self._dist, citem[item])

        # Obviously it's possible to get away with half of the work here.
        # Let's focus on correct results first and optimize later.
        xt = self._transform(x, loc, scale)
        fx = f(xt, *args, **kwargs)
        cfx = cf(xt, *args, **kwargs)
        return np.where(sign, fx, cfx)[()]

    return wrapped

