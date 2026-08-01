
def sample_inputs_max_min_reduction_with_dim(op_info, device, dtype, requires_grad, **kwargs):
    args_for_reduction_with_dim = (
        ((S, S, S), (1,),),
        ((S, S, S), (1, True, ),),
        ((), (0,),),
        ((), (0, True,),),
    )
    return ((SampleInput(make_tensor(input_tensor, dtype=dtype, device=device,
                                     low=None, high=None,
                                     requires_grad=requires_grad),
                         *args))
            for input_tensor, args in args_for_reduction_with_dim)

