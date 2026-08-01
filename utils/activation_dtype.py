
def activation_dtype(qconfig):
    if qconfig is None:
        raise AssertionError("qconfig must be provided to determine activation dtype")
    activation = qconfig.activation()
    return activation.dtype

