
def sample_inputs_chunk_cat(op_info, device, dtype, requires_grad, **kwargs):
    # 1. If input tensors have different ndims, dim should be non-negative and be less than the ndims of every input tensors.
    #    If all input tensors have the same ndims, we support both negative and non-negative dim.
    # 2. For wrapped_dim, all tensors should have the same size for 0,...,wrapped_dim-1 dimensions.
    #        No requirements for (wrapped_dim, ...)-th dimension.
    # 3. Expect positive num_chunks
    # 4. Expect non-empty input tensor list and each input tensor should have at least 1 element
    # 5. Non-contiguous input tensors are allowed.
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    same_ndim_cases = (
        (
            [
                torch.Size([1, 2, 3]),
                torch.Size([1, 2, 3]),
            ], -1, 5
        ),
        (
            [
                torch.Size([1, 2, 129]),
                torch.Size([1, 2, 297]),
            ], -1, 5
        ),
        (
            [
                torch.Size([1, 2, 3]),
                torch.Size([1, 2, 3]),
            ], 1, 5
        ),
        (
            [
                torch.Size([3, 3, 2, 1]),
                torch.Size([1, 4, 2, 2]),
                torch.Size([2, 1, 3, 3]),
            ], 0, 2
        ),
    )
    for sizes, dim, num_chunks in same_ndim_cases:
        tensors = [make_arg(size) for size in sizes]
        yield SampleInput(tensors, args=(dim, num_chunks))

    different_ndim_case = [
        torch.Size([2, 3, 3]),
        torch.Size([2, 3, 1, 2]),
        torch.Size([2, 3]),
        torch.Size([2, 3, 2]),
        torch.Size([2, 3, 271]),
    ]
    max_dim, num_chunks = 2, 3
    for dim in range(max_dim):
        tensors = []
        for size in different_ndim_case:
            tensors.append(make_arg(size))
        yield SampleInput(tensors, args=(dim, num_chunks))

    # non-contiguous
    for dim in range(max_dim):
        tensors = []
        for size in different_ndim_case:
            # make the last 2 dims column-major (i.e. non-contiguous)
            t = make_arg(size).transpose(-2, -1).contiguous().transpose(-2, -1)
            tensors.append(t)
        yield SampleInput(tensors, args=(dim, num_chunks))

