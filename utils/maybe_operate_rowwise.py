
def maybe_operate_rowwise(func: F) -> F:
    """
    NumPy operations on C-contiguous ndarrays with axis=1 can be
    very slow if axis 1 >> axis 0.
    Operate row-by-row and concatenate the results.
    """

    @functools.wraps(func)
    def newfunc(values: np.ndarray, *, axis: AxisInt | None = None, **kwargs):
        if (
            axis == 1
            and values.ndim == 2
            and values.flags["C_CONTIGUOUS"]
            # only takes this path for wide arrays (long dataframes), for threshold see
            # https://github.com/pandas-dev/pandas/pull/43311#issuecomment-974891737
            and (values.shape[1] / 1000) > values.shape[0]
            and values.dtype not in (object, bool)
        ):
            arrs = list(values)
            if kwargs.get("mask") is not None:
                mask = kwargs.pop("mask")
                results = [
                    func(arrs[i], mask=mask[i], **kwargs) for i in range(len(arrs))
                ]
            else:
                results = [func(x, **kwargs) for x in arrs]
            return np.array(results)

        return func(values, axis=axis, **kwargs)

    return cast(F, newfunc)

