
def _validate_gpass_gstop(gpass, gstop):

    if gpass <= 0.0:
        raise ValueError("gpass should be larger than 0.0")
    elif gstop <= 0.0:
        raise ValueError("gstop should be larger than 0.0")
    elif gpass > gstop:
        raise ValueError("gpass should be smaller than gstop")

