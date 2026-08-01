
def _array2string(a, options, separator=' ', prefix=""):
    # The formatter __init__s in _get_format_function cannot deal with
    # subclasses yet, and we also need to avoid recursion issues in
    # _formatArray with subclasses which return 0d arrays in place of scalars
    data = asarray(a)
    if a.shape == ():
        a = data

    if a.size > options['threshold']:
        summary_insert = "..."
        data = _leading_trailing(data, options['edgeitems'])
    else:
        summary_insert = ""

    # find the right formatting function for the array
    format_function = _get_format_function(data, **options)

    # skip over "["
    next_line_prefix = " "
    # skip over array(
    next_line_prefix += " " * len(prefix)

    lst = _formatArray(a, format_function, options['linewidth'],
                       next_line_prefix, separator, options['edgeitems'],
                       summary_insert, options['legacy'])
    return lst

