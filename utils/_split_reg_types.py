
def _split_reg_types(reg_types_str: str):
    """
    Split on underscores but append "_t" to the previous element.
    """
    tokens = reg_types_str.split("_")
    reg_types = []
    for token in tokens:
        if token == "t" and len(reg_types) > 0:
            reg_types[-1] += "_t"
        else:
            reg_types += [token]
    return reg_types

