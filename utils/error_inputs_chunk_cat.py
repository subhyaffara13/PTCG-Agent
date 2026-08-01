
def error_inputs_chunk_cat(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # input tensors have different ndims but dim is negative
    sizes, dim, num_chunks = [torch.Size([2, 3]), torch.Size([4,])], -1, 3
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects non-negative dim when input tensors have different ndims',
    )

    # input tensors have different ndims but dim >= ndim of some input tensors
    sizes, dim, num_chunks = [torch.Size([2, 3]), torch.Size([4,])], 1, 3
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects dim < ndim for all input tensors',
    )

    # some tensors have different sizes for 0, ..., dim-1 dimensions.
    sizes, dim, num_chunks = [torch.Size([2, 3, 4]), torch.Size([4, 3])], 1, 3
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects same sizes of 0,...,dim-1 dimensions for all tensors',
    )

    # negative num_chunks
    sizes, dim, num_chunks = [torch.Size([2,]), torch.Size([3,])], 0, -1
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects positive num_chunks',
    )

    # zero as num_chunks
    sizes, dim, num_chunks = [torch.Size([2,]), torch.Size([3,])], 0, 0
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects positive num_chunks',
    )

    # empty input tensor list
    dim, num_chunks = 0, 1
    yield ErrorInput(
        SampleInput([], args=(dim, num_chunks)),
        error_regex='_chunk_cat expects a non-empty input tensor list',
    )

    # empty input tensor with 0 elements
    sizes, dim, num_chunks = [torch.Size([0,]), torch.Size([3,])], 0, 1
    tensors = [make_arg(size) for size in sizes]
    yield ErrorInput(
        SampleInput(tensors, args=(dim, num_chunks)),
        error_regex='_chunk_cat expects non-empty tensor',
    )

