
def _dtype_test_suffix(dtypes):
    """Returns the test suffix for a dtype, sequence of dtypes, or None."""
    if isinstance(dtypes, (list, tuple)):
        if len(dtypes) == 0:
            return ""
        return "_" + "_".join(dtype_name(d) for d in dtypes)
    elif dtypes:
        return f"_{dtype_name(dtypes)}"
    else:
        return ""

