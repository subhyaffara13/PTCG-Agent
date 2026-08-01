
def _guess_datetime_format_for_array(arr, dayfirst: bool | None = False) -> str | None:
    # Try to guess the format based on the first non-NaN element, return None if can't
    if (first_non_null := tslib.first_non_null(arr)) != -1:
        if type(first_non_nan_element := arr[first_non_null]) is str:
            # GH#32264 np.str_ object
            guessed_format = guess_datetime_format(
                first_non_nan_element, dayfirst=dayfirst
            )
            if guessed_format is not None:
                return guessed_format
            # If there are multiple non-null elements, warn about
            # how parsing might not be consistent
            if tslib.first_non_null(arr[first_non_null + 1 :]) != -1:
                warnings.warn(
                    "Could not infer format, so each element will be parsed "
                    "individually, falling back to `dateutil`. To ensure parsing is "
                    "consistent and as-expected, please specify a format.",
                    UserWarning,
                    stacklevel=find_stack_level(),
                )
    return None

