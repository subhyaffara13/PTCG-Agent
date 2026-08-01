
def _shift_scale_inverse_function(func):
    citem = {'_ilogcdf_dispatch': '_ilogccdf_dispatch',
             '_icdf_dispatch': '_iccdf_dispatch',
             '_ilogccdf_dispatch': '_ilogcdf_dispatch',
             '_iccdf_dispatch': '_icdf_dispatch'}
    def wrapped(self, p, *args, loc, scale, sign, **kwargs):
        item = func.__name__

        f = getattr(self._dist, item)
        cf = getattr(self._dist, citem[item])

        # Obviously it's possible to get away with half of the work here.
        # Let's focus on correct results first and optimize later.
        fx =  self._itransform(f(p, *args, **kwargs), loc, scale)
        cfx = self._itransform(cf(p, *args, **kwargs), loc, scale)
        return np.where(sign, fx, cfx)[()]

    return wrapped

