
def get_qconfig_dtypes(qconfig):
    r"""returns the qconfig tuple for qconfig:
    (activation_dtype, weight_dtype, activation_is_dynamic)
    """
    if qconfig is None:
        raise AssertionError("qconfig must be provided to extract dtypes")
    activation = qconfig.activation()
    weight = qconfig.weight()
    act_is_dynamic = getattr(activation, "is_dynamic", False)
    return (activation.dtype, weight.dtype, act_is_dynamic)

