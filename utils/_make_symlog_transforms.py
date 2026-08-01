
def _make_symlog_transforms(c: float = 1, base: float = 10) -> TransFuncs:

    # From https://iopscience.iop.org/article/10.1088/0957-0233/24/2/027001

    # Note: currently not using base because we only get
    # one parameter from the string, and are using c (this is consistent with d3)

    log, exp = _make_log_transforms(base)

    def symlog(x):
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.sign(x) * log(1 + np.abs(np.divide(x, c)))

    def symexp(x):
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.sign(x) * c * (exp(np.abs(x)) - 1)

    return symlog, symexp

