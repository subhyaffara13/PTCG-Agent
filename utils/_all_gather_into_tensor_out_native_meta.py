
def _all_gather_into_tensor_out_native_meta(input, group_size, group_name, *, out):
    return _make_all_gather_out_tensor(input, group_size)

