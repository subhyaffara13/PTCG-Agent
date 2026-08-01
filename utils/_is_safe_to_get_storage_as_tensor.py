
def _is_safe_to_get_storage_as_tensor(tensor: torch.Tensor) -> bool:
    # This function checks if a nested tensor is valid for
    # use with the flash-attention and efficient_attention kernels without
    # needing to call contiguous on the nested tensor input.
    # It checks that the storage offsets' adjacent_differences are a constant
    # multiple of the previous tensor in the nested tensor and that the strides
    # are monitonically decreasing. This check is done after calling transpose on
    # the nested tensor resulting in a Nt of shape [bsz, {seq_len}, num_heads, dim]

    # Returns a boolean indicating if contiguous needs to be called for input
    if not isinstance(tensor, NestedTensor):
        raise AssertionError("tensor must be a NestedTensor")
    offsets = tensor.offsets()
    strides = tensor._strides

    n_tensors = offsets.size(0) - 1
    if n_tensors <= 1:
        return True

    # Check initially that the tensor strides are in strictly descending order
    prev_stride = strides[1]
    for stride in strides[2:]:
        if prev_stride <= stride:
            # This would mean that the last stride is greater than the seq_len
            # stride
            return False
        prev_stride = stride

    # Congrats you made it!
    return True

