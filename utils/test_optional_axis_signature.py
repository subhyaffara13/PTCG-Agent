
def test_optional_axis_signature():
    # There are three types of original signatures possible, and this only tests one
    # example class of each:
    # 1. `axis` without default: LinearScale, FuncScale, FuncScaleLog
    # 2. `axis` with default and more positional parameters: LogitScale
    # 3. `axis` with default and only keyword-only parameters: LogScale, AsinhScale,
    #    SymmetricalLogScale
    # Testing with None is sufficient as detection is purely based on the
    # signature structure; no type information is involved.
    axis = None

    # Old signature with axis positionally.
    FuncScale(axis, (lambda x: x, lambda x: x))
    FuncScale(axis, functions=(lambda x: x, lambda x: x))
    LogitScale(axis)
    LogitScale(axis, 'clip')
    LogitScale(axis, nonpositive='clip')
    LogitScale(axis, use_overline=True)
    AsinhScale(axis)
    AsinhScale(axis, linear_width=2)
    AsinhScale(axis, base=3)
    AsinhScale(axis, subs=[2, 6])
    # Old signature with axis as keyword.
    FuncScale(axis=axis, functions=(lambda x: x, lambda x: x))
    LogitScale(axis=axis)
    LogitScale(axis=axis, nonpositive='clip')
    LogitScale(axis=axis, use_overline=True)
    AsinhScale(axis=axis)
    AsinhScale(axis=axis, linear_width=2)
    AsinhScale(axis=axis, base=3)
    AsinhScale(axis=axis, subs=[2, 6])
    # New signature without axis.
    FuncScale((lambda x: x, lambda x: x))
    FuncScale(functions=(lambda x: x, lambda x: x))
    LogitScale()
    LogitScale(nonpositive='clip')
    LogitScale(use_overline=True)
    AsinhScale()
    AsinhScale(linear_width=2)
    AsinhScale(base=3)
    AsinhScale(subs=[2, 6])

