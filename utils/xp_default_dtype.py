
def xp_default_dtype(xp):
    """Query the namespace-dependent default floating-point dtype.
    """
    if is_torch(xp):
        # historically, we allow pytorch to keep its default of float32
        return xp.get_default_dtype()
    else:
        # we default to float64
        return xp.float64

