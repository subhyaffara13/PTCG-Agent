
def has_corresponding_torch_dtype(np_dtype):
    try:
        numpy_to_torch_dtype(np_dtype)
        return True
    except KeyError:
        return False

