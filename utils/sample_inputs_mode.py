
def sample_inputs_mode(op_info, device, dtype, requires_grad, **kwargs):
    args = (
        ((S, S, S), (),),
        ((S, S, S), (1, ),),
        ((S, S, S), (1, True, ),),
        ((), (),),
        ((), (0,),),
        ((), (0, True,),),
        # Non-fused mode kernel on CUDA
        ((3000,), ()),
    )
    make_arg = partial(make_tensor, dtype=dtype, device=device,
                       requires_grad=requires_grad, low=None, high=None)
    return (SampleInput(make_arg(input_tensor), *args)
            for input_tensor, args in args)

