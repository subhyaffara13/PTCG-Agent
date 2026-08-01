
def _fix_defaults(output, defaults=None):
    """
    Update the fill_value and masked data of `output`
    from the default given in a dictionary defaults.
    """
    names = output.dtype.names
    (data, mask, fill_value) = (output.data, output.mask, output.fill_value)
    for (k, v) in (defaults or {}).items():
        if k in names:
            fill_value[k] = v
            data[k][mask[k]] = v
    return output

