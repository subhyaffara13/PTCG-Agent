
def module_inputs_torch_nn_InstanceNormNd(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    lazy = kwargs.get('lazy', False)
    N = kwargs['N']
    num_features, eps, momentum, affine, track_running_stats = 3, 1e-3, 0.3, False, True
    input_no_batch_shape_dict = {1: (3, 15), 2: (3, 6, 6), 3: (3, 4, 4, 4)}
    input_no_batch_shape = input_no_batch_shape_dict[N]
    input_batch_shape = (4,) + input_no_batch_shape

    return [
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum) if lazy else FunctionInput(num_features, eps, momentum)
            ),
            forward_input=FunctionInput(make_input(input_batch_shape))),
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum, affine, track_running_stats) if lazy else
                FunctionInput(num_features, eps, momentum, affine, track_running_stats)
            ),
            forward_input=FunctionInput(make_input(input_batch_shape)),
            desc='tracking_stats'),
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum) if lazy else FunctionInput(num_features, eps, momentum)
            ),
            forward_input=FunctionInput(make_input(input_no_batch_shape)),
            reference_fn=no_batch_dim_reference_fn,
            desc='tracking_stats_no_batch_dim'),
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum, affine, track_running_stats) if lazy else
                FunctionInput(num_features, eps, momentum, affine, track_running_stats)
            ),
            forward_input=FunctionInput(make_input(input_no_batch_shape)),
            reference_fn=no_batch_dim_reference_fn,
            desc='no_batch_dim'),
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum, affine=True) if lazy else
                FunctionInput(num_features, eps, momentum, affine=True)
            ),
            forward_input=FunctionInput(make_input(input_batch_shape)),
            desc='affine'),
        ModuleInput(
            constructor_input=(
                FunctionInput(eps, momentum, affine=True, bias=False) if lazy else
                FunctionInput(num_features, eps, momentum, affine=True, bias=False)
            ),
            forward_input=FunctionInput(make_input(input_batch_shape)),
            desc='affine_not_bias'),]

