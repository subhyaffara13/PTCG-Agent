
def _clean_na_values(na_values, keep_default_na: bool = True, floatify: bool = True):
    na_fvalues: set | dict
    if na_values is None:
        if keep_default_na:
            na_values = STR_NA_VALUES
        else:
            na_values = set()
        na_fvalues = set()
    elif isinstance(na_values, dict):
        old_na_values = na_values.copy()
        na_values = {}  # Prevent aliasing.

        # Convert the values in the na_values dictionary
        # into array-likes for further use. This is also
        # where we append the default NaN values, provided
        # that `keep_default_na=True`.
        for k, v in old_na_values.items():
            if not is_list_like(v):
                v = [v]

            if keep_default_na:
                v = set(v) | STR_NA_VALUES

            na_values[k] = _stringify_na_values(v, floatify)
        na_fvalues = {k: _floatify_na_values(v) for k, v in na_values.items()}
    else:
        if not is_list_like(na_values):
            na_values = [na_values]
        na_values = _stringify_na_values(na_values, floatify)
        if keep_default_na:
            na_values = na_values | STR_NA_VALUES

        na_fvalues = _floatify_na_values(na_values)

    return na_values, na_fvalues

