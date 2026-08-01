
def compare_op(series, other, op):
    left = np.abs(series) if op in (ops.rpow, operator.pow) else series
    right = np.abs(other) if op in (ops.rpow, operator.pow) else other

    cython_or_numpy = op(left, right)
    python = left.combine(right, op)
    if isinstance(other, Series) and not other.index.equals(series.index):
        python.index = python.index._with_freq(None)
    tm.assert_series_equal(cython_or_numpy, python)

