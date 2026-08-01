
def error_inputs_max_unpool(op_info, device, **kwargs):
    """Error inputs for max_unpool: shape mismatch between input and indices."""
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)
    pool_dim = _UNPOOL_NAME_TO_DIM[op_info.name]

    # Create mismatched shapes for input and indices
    kwargs_dict = {'kernel_size': 3, 'stride': 2, 'padding': 0}
    if pool_dim == 1:
        input_shape = (8, 8)
        indices_shape = (8, 7)
    elif pool_dim == 2:
        input_shape = (1, 1, 4, 4)
        indices_shape = (1, 1, 4, 1)
    else:  # pool_dim == 3
        input_shape = (1, 1, 4, 4, 4)
        indices_shape = (1, 1, 4, 4, 1)

    yield ErrorInput(
        SampleInput(
            make_arg(input_shape),
            args=(torch.zeros(indices_shape, device=device, dtype=torch.long),),
            kwargs=kwargs_dict
        ),
        error_type=RuntimeError,
        error_regex='Expected shape of indices to be'
    )

