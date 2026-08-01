
def _dict_formatter(d, n=0, mplus=1, sorter=None):
    """
    Pretty printer for dictionaries

    `n` keeps track of the starting indentation;
    lines are indented by this much after a line break.
    `mplus` is additional left padding applied to keys
    """
    if isinstance(d, dict):
        m = max(map(len, list(d.keys()))) + mplus  # width to print keys
        s = '\n'.join([k.rjust(m) + ': ' +  # right justified, width m
                       _indenter(_dict_formatter(v, m+n+2, 0, sorter), m+2)
                       for k, v in sorter(d)])  # +2 for ': '
    else:
        # By default, NumPy arrays print with linewidth=76. `n` is
        # the indent at which a line begins printing, so it is subtracted
        # from the default to avoid exceeding 76 characters total.
        # `edgeitems` is the number of elements to include before and after
        # ellipses when arrays are not shown in full.
        # `threshold` is the maximum number of elements for which an
        # array is shown in full.
        # These values tend to work well for use with OptimizeResult.
        with np.printoptions(linewidth=76-n, edgeitems=2, threshold=12,
                             formatter={'float_kind': _float_formatter_10}):
            s = str(d)
    return s

