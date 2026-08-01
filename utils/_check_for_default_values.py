
def _check_for_default_values(fname, arg_val_dict, compat_args) -> None:
    """
    Check that the keys in `arg_val_dict` are mapped to their
    default values as specified in `compat_args`.

    Note that this function is to be called only when it has been
    checked that arg_val_dict.keys() is a subset of compat_args
    """
    for key in arg_val_dict:
        # try checking equality directly with '=' operator,
        # as comparison may have been overridden for the left
        # hand object
        try:
            v1 = arg_val_dict[key]
            v2 = compat_args[key]

            # check for None-ness otherwise we could end up
            # comparing a numpy array vs None
            if (v1 is not None and v2 is None) or (v1 is None and v2 is not None):
                match = False
            else:
                match = v1 == v2

            if not is_bool(match):
                raise ValueError("'match' is not a boolean")

        # could not compare them directly, so try comparison
        # using the 'is' operator
        except ValueError:
            match = arg_val_dict[key] is compat_args[key]

        if not match:
            raise ValueError(
                f"the '{key}' parameter is not supported in "
                f"the pandas implementation of {fname}()"
            )

