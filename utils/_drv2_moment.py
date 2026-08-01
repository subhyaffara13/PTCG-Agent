
def _drv2_moment(self, n, *args):
    """Non-central moment of discrete distribution."""
    def fun(x):
        return np.power(x, n) * self._pmf(x, *args)

    _a, _b = self._get_support(*args)
    return _expect(fun, _a, _b, self._ppf(0.5, *args), self.inc)

