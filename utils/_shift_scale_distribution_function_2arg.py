
def _shift_scale_distribution_function_2arg(func):
    def wrapped(self, x, y, *args, loc, scale, sign, **kwargs):
        item = func.__name__

        f = getattr(self._dist, item)

        # Obviously it's possible to get away with half of the work here.
        # Let's focus on correct results first and optimize later.
        xt = self._transform(x, loc, scale)
        yt = self._transform(y, loc, scale)
        fxy = f(xt, yt, *args, **kwargs)
        fyx = f(yt, xt, *args, **kwargs)
        return np.real_if_close(np.where(sign, fxy, fyx))[()]

    return wrapped

