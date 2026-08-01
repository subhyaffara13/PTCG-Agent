
def _make_log_transforms(base: float | None = None) -> TransFuncs:

    fs: TransFuncs
    if base is None:
        fs = np.log, np.exp
    elif base == 2:
        fs = np.log2, partial(np.power, 2)
    elif base == 10:
        fs = np.log10, partial(np.power, 10)
    else:
        def forward(x):
            return np.log(x) / np.log(base)
        fs = forward, partial(np.power, base)

    def log(x: ArrayLike) -> ArrayLike:
        with np.errstate(invalid="ignore", divide="ignore"):
            return fs[0](x)

    def exp(x: ArrayLike) -> ArrayLike:
        with np.errstate(invalid="ignore", divide="ignore"):
            return fs[1](x)

    return log, exp

