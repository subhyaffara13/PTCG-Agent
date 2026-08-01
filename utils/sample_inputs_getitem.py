
def sample_inputs_getitem(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    test_args = [
        ([1, 2],),
        (slice(0, 3),),
        ((slice(0, 3), 1),),
        (([0, 2, 3], [1, 3, 3], [0, 0, 2]),),
        (([0, 0, 3], [1, 1, 3], [0, 0, 2]),),
        ((slice(None), slice(None), [0, 3]),),
        ((slice(None), [0, 3], slice(None)),),
        (([0, 3], slice(None), slice(None)),),
        (([0, 3], [1, 2], slice(None)),),
        (([0, 3], ),),
        (([0, 3], slice(None)),),
        (([0, 3], Ellipsis),),
        (([0, 2, 3], [1, 3, 3], torch.LongTensor([0, 0, 2])),),
        (index_variable(2, S, device=device),),
        (mask_not_all_zeros((S,)),),
    ]

    for args in test_args:
        yield SampleInput(make_arg((S, S, S)), args=args)

    yield SampleInput(make_arg((S, S, S, S)), args=((slice(None), [0, 1], slice(None), [0, 1]),))

