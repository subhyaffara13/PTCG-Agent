
def sample_inputs_tril_triu(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    cases = (((M, M), ()),
             ((M, M), (2,),),
             ((M, S), ()),
             ((M, S), (-1,)),
             ((M, M), (2,),),
             ((S, M, S), ()),
             ((S, M, S), (2,)),
             ((3, 3, S, S), ()),)

    for shape, args in cases:
        yield SampleInput(make_arg(shape), args=args)

