
def sample_inputs_max_unpool(op_info, device, dtype, requires_grad, **kwargs):
    unpool_name_to_pool_method_dict = {
        'nn.functional.max_unpool1d': torch.nn.functional.max_pool1d,
        'nn.functional.max_unpool2d': torch.nn.functional.max_pool2d,
        'nn.functional.max_unpool3d': torch.nn.functional.max_pool3d
    }

    unpool_to_pool_name_dict = {k: f'nn.functional.{v.__name__}' for k, v in unpool_name_to_pool_method_dict.items()}

    pool_dim = _UNPOOL_NAME_TO_DIM[op_info.name]
    pool_method = unpool_name_to_pool_method_dict[op_info.name]

    pool_op_info = copy.copy(op_info)
    pool_op_info.name = unpool_to_pool_name_dict[op_info.name]

    for sample in sample_inputs_max_pool(pool_op_info, device, dtype, requires_grad, **kwargs):
        # shapes (C, ...) do not work as of now,
        # see https://github.com/pytorch/pytorch/issues/68337
        # TODO: remove once the issue is resolved
        if sample.input.dim() != pool_dim + 2:
            continue

        # No dilation > 1 for max_unpool,
        # see https://github.com/pytorch/pytorch/issues/68420
        if sample.kwargs['dilation'] != 1:
            continue

        # Can't unpool without indices
        if sample.kwargs['return_indices']:
            pool, indices = pool_method(sample.input, **sample.kwargs)
            # arg has to be a leaf
            arg = pool.detach().requires_grad_(requires_grad)
            sample_kwargs = {
                'kernel_size': sample.kwargs['kernel_size'],
                'stride': sample.kwargs['stride'],
                'padding': sample.kwargs['padding'],
                # output_size could be None but we specify it explicitly
                # to compensate for the information lose in pool due
                # to the floor/ceil operation used to compute the shapes
                'output_size': sample.input.size()
            }

            yield SampleInput(arg, args=(indices,), kwargs=sample_kwargs)

