
def _get_dtype_of(obj):
    """ Convert the argument for *_fill_value into a dtype """
    if isinstance(obj, np.dtype):
        return obj
    elif hasattr(obj, 'dtype'):
        return obj.dtype
    else:
        return np.asanyarray(obj).dtype

