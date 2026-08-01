
def _standardize_out_kwarg(**kwargs) -> dict:
    """
    If kwargs contain "out1" and "out2", replace that with a tuple "out"

    np.divmod, np.modf, np.frexp can have either `out=(out1, out2)` or
    `out1=out1, out2=out2)`
    """
    if "out" not in kwargs and "out1" in kwargs and "out2" in kwargs:
        out1 = kwargs.pop("out1")
        out2 = kwargs.pop("out2")
        out = (out1, out2)
        kwargs["out"] = out
    return kwargs

