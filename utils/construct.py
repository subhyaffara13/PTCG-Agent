
def construct(t):
    """ Turn a Compound into a SymPy object """
    if isinstance(t, (Variable, CondVariable)):
        return t.arg
    if not isinstance(t, Compound):
        return t
    if any(issubclass(t.op, cls) for cls in eval_false_legal):
        return t.op(*map(construct, t.args), evaluate=False)
    elif any(issubclass(t.op, cls) for cls in basic_new_legal):
        return Basic.__new__(t.op, *map(construct, t.args))
    else:
        return t.op(*map(construct, t.args))


def construct(box, shape, value=None, dtype=None, **kwargs):
    """
    construct an object for the given shape
    if value is specified use that if its a scalar
    if value is an array, repeat it as needed
    """
    if isinstance(shape, int):
        shape = tuple([shape] * box._AXIS_LEN)
    if value is not None:
        if is_scalar(value):
            if value == "empty":
                arr = None
                dtype = np.float64

                # remove the info axis
                kwargs.pop(box._info_axis_name, None)
            else:
                arr = np.empty(shape, dtype=dtype)
                arr.fill(value)
        else:
            fshape = np.prod(shape)
            arr = value.ravel()
            new_shape = fshape / arr.shape[0]
            if fshape % arr.shape[0] != 0:
                raise Exception("invalid value passed in construct")

            arr = np.repeat(arr, new_shape).reshape(shape)
    else:
        arr = np.random.default_rng(2).standard_normal(shape)
    return box(arr, dtype=dtype, **kwargs)

