
def maybe_unbox_numpy_scalar(value):
    result = value
    if using_python_scalars() and isinstance(value, np.generic):
        if isinstance(result, np.longdouble):
            result = float(result)
        elif isinstance(result, np.complex256):
            result = complex(result)
        elif isinstance(result, np.datetime64):
            result = Timestamp(result)
        elif isinstance(result, np.timedelta64):
            result = Timedelta(result)
        else:
            result = value.item()
    return result

