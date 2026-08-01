
def _all_gather_into_tensor_coalesced_native_meta(inputs, group_size, group_name):
    return [
        _all_gather_into_tensor_native_meta(input, group_size, group_name)
        for input in inputs
    ]

