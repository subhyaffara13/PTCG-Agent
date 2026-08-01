
def dtype_name(dtype):
    """ Returns the pretty name of the dtype (e.g. torch.int64 -> int64). """
    return str(dtype).split('.')[1]

