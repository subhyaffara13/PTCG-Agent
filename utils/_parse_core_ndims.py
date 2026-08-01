
def _parse_core_ndims(signature):
    """Return tuple of num core dims per input from gufunc signature."""
    input_sig = signature.split('->')[0]
    groups = re.findall(r"\((.*?)\)", input_sig)
    return tuple(0 if not g.strip() else g.count(',') + 1 for g in groups)

