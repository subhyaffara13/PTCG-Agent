
def _get_input_to_perturb(input):
    # Prepare the input so that it can be modified in-place and do certain
    # operations that require the tensor to have strides. If fast_mode=False,
    # _iter_tensor would handle the below cases:
    if input.layout == torch._mkldnn:  # type: ignore[attr-defined] # no attr _mkldnn
        # Convert to dense so we can perform operations that require strided tensors
        input_to_perturb = input.to_dense()
    elif _is_sparse_any_tensor(input):
        # Clone because input may require grad, and copy_ calls resize_,
        # which is not allowed for .data
        input_to_perturb = input.clone()
    else:
        input_to_perturb = input.data
    return input_to_perturb

