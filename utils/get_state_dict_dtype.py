
def get_state_dict_dtype(state_dict):
    """
    Returns the first found floating dtype in `state_dict` if there is one, otherwise returns the first dtype.
    """
    for t in state_dict.values():
        # We cannot instantiate a whole model under float4/8_xxx dtypes (torch does not allow setting them as default dtype)
        if t.is_floating_point() and "float8_" not in str(t.dtype) and "float4_" not in str(t.dtype):
            return t.dtype

    # if no floating dtype was found return whatever the first dtype is
    if len(state_dict) == 0:
        return torch.float32
    return next(iter(state_dict.values())).dtype

