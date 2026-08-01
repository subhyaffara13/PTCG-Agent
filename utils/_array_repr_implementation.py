
def _array_repr_implementation(
        arr, max_line_width=None, precision=None, suppress_small=None,
        array2string=array2string):
    """Internal version of array_repr() that allows overriding array2string."""
    current_options = format_options.get()
    override_repr = current_options["override_repr"]
    if override_repr is not None:
        return override_repr(arr)

    if max_line_width is None:
        max_line_width = current_options['linewidth']

    if type(arr) is not ndarray:
        class_name = type(arr).__name__
    else:
        class_name = "array"

    prefix = class_name + "("
    if (current_options['legacy'] <= 113 and
            arr.shape == () and not arr.dtype.names):
        lst = repr(arr.item())
    else:
        lst = array2string(arr, max_line_width, precision, suppress_small,
                           ', ', prefix, suffix=")")

    # Add dtype and shape information if these cannot be inferred from
    # the array string.
    extras = []
    if ((arr.size == 0 and arr.shape != (0,))
            or (current_options['legacy'] > 210
            and arr.size > current_options['threshold'])):
        extras.append(f"shape={arr.shape}")
    if not dtype_is_implied(arr.dtype) or arr.size == 0:
        extras.append(f"dtype={dtype_short_repr(arr.dtype)}")

    if not extras:
        return prefix + lst + ")"

    arr_str = prefix + lst + ","
    extra_str = ", ".join(extras) + ")"
    # compute whether we should put extras on a new line: Do so if adding the
    # extras would extend the last line past max_line_width.
    # Note: This line gives the correct result even when rfind returns -1.
    last_line_len = len(arr_str) - (arr_str.rfind('\n') + 1)
    spacer = " "
    if current_options['legacy'] <= 113:
        if issubclass(arr.dtype.type, flexible):
            spacer = '\n' + ' ' * len(prefix)
    elif last_line_len + len(extra_str) + 1 > max_line_width:
        spacer = '\n' + ' ' * len(prefix)

    return arr_str + spacer + extra_str

