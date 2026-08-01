
def dispatch_reduction_ufunc(self, ufunc: np.ufunc, method: str, *inputs, **kwargs):
    """
    Dispatch ufunc reductions to self's reduction methods.
    """
    assert method == "reduce"

    if len(inputs) != 1 or inputs[0] is not self:
        return NotImplemented

    if ufunc.__name__ not in REDUCTION_ALIASES:
        return NotImplemented

    method_name = REDUCTION_ALIASES[ufunc.__name__]

    # NB: we are assuming that min/max represent minimum/maximum methods,
    #  which would not be accurate for e.g. Timestamp.min
    if not hasattr(self, method_name):
        return NotImplemented

    if self.ndim > 1:
        if isinstance(self, ABCNDFrame):
            # TODO: test cases where this doesn't hold, i.e. 2D DTA/TDA
            kwargs["numeric_only"] = False

        if "axis" not in kwargs:
            # For DataFrame reductions we don't want the default axis=0
            # Note: np.min is not a ufunc, but uses array_function_dispatch,
            #  so calls DataFrame.min (without ever getting here) with the np.min
            #  default of axis=None, which DataFrame.min catches and changes to axis=0.
            # np.minimum.reduce(df) gets here bc axis is not in kwargs,
            #  so we set axis=0 to match the behavior of np.minimum.reduce(df.values)
            kwargs["axis"] = 0

    # By default, numpy's reductions do not skip NaNs, so we have to
    #  pass skipna=False
    result = getattr(self, method_name)(skipna=False, **kwargs)
    result = maybe_unbox_numpy_scalar(result)
    return result

