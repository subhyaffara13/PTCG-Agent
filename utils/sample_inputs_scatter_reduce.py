
def sample_inputs_scatter_reduce(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    gather = partial(gather_variable, device=device)

    zero = torch.tensor(0, dtype=torch.long, device=device)
    test_cases = (
        ((M, S), 0, gather((S, S), 1, M), (S, S)),
        ((M, S), 1, gather((S, S), 0, S), (S, S)),
        ((M, S), -1, gather((S, S), 0, S), (S, S)),
        ((M, S), 0, gather((M, S // 2), 1, M), (M, S // 2)),
        ((M, S), 1, gather((M, S // 2), 0, S), (M, S // 2)),
        ((M, S), -1, gather((M, S // 2), 0, S), (M, S // 2)),
        ((), 0, zero.detach().clone(), ()),
    )

    reduce = op_info.variant_test_name
    for (inp_shape, dim, index, src_shape), include_self in product(test_cases, [False, True, False]):
        yield SampleInput(make_arg(inp_shape),
                          args=(dim, index, make_arg(src_shape), reduce),
                          kwargs={'include_self': include_self})


    # Sample inputs to test edge cases for backward
    # Check that gradients are propagated correctly for prod when zeros in self/src are reduced
    if requires_grad and reduce == 'prod':
        # This sample tests gradients for the following cases
        # (a) 1 zero reduced (from src (self[0, 1], self[1, 1]), from self (self[0, 0], self[2, 0]))
        # (b) 2 zeros reduced (1 from src and 1 from self (self[1, 0])
        # (c) no zeros reduced (self([2, 1]))
        # (d) 2 zeros reduced (both from src) is tested in test/test_autograd.py
        #     test_scatter_index_reduce_prod_gradgrad_error as this case is not supported for gradgrad
        input = torch.tensor([[0, 13], [0, 17], [0, 19]], dtype=dtype, device=device, requires_grad=requires_grad)
        src = torch.tensor([[0, 1, 2, 3], [0, 4, 0, 1], [2, 3, 5, 6]], dtype=dtype, device=device, requires_grad=requires_grad)
        idx = torch.tensor([[1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]], dtype=torch.long, device=device)

        yield SampleInput(input,
                          args=(1, idx, src, reduce),
                          kwargs={'include_self': True})

