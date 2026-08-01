
def weight_dtype(qconfig):
    if qconfig is None:
        raise AssertionError("qconfig must be provided to determine weight dtype")
    weight = qconfig.weight()
    return weight.dtype

