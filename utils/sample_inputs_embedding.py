
def sample_inputs_embedding(op_info, device, dtype, requires_grad, **kwargs):
    def make_input(shape):
        return make_tensor(shape, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_long_input(shape, *, low, high):
        return make_tensor(shape, device=device, dtype=torch.long, low=low, high=high)

    # 0-D index tensor
    idx = make_long_input((), low=0, high=M)
    yield SampleInput(make_input((M, S)), args=(idx,),)

    # 1-D index tensor
    idx = make_long_input((S,), low=0, high=M)
    yield SampleInput(make_input((M, S)), args=(idx,),)

    # 2-D index tensor
    idx = make_long_input((S, S), low=0, high=M)
    yield SampleInput(make_input((M, S)), args=(idx,),)

    if not requires_grad:
        # Following inputs return different gradient from the numerical gradient.
        # This is expected and relevant tests are present in `test_nn.py`.

        # The gradient vector at `padding_idx` is not updated.
        idx = make_long_input((2, 2), low=0, high=S)
        idx[0, 0] = 2
        idx[1, 1] = 2
        yield SampleInput(make_input((S, S)), args=(idx,), kwargs={'padding_idx': 2},)

        idx = make_long_input((2, 2), low=0, high=S)
        idx[0, 0] = 4
        idx[1, 1] = 4
        yield SampleInput(make_input((S, S)), args=(idx,), kwargs={'padding_idx': -1},)

        # Due to inplace renorming of weight, the numerical gradient doesn't match the
        # analytical gradient.
        idx = make_long_input((2, 2), low=0, high=S)
        weights = make_input((S, S)) * 2
        yield SampleInput(weights, args=(idx,), kwargs={'max_norm': 1.},)

        idx = make_long_input((2, 2), low=0, high=S)
        weights = make_input((S, S)) * 2
        yield SampleInput(weights, args=(idx,), kwargs={'max_norm': 1., 'norm_type': 1.0},)

        # Scale the gradient based on the inverse frequency of a particular index.
        idx = make_long_input((2, 2), low=0, high=S)
        idx[0, 0] = 1
        idx[0, 1] = 1
        weights = make_input((S, S))
        yield SampleInput(weights, args=(idx,), kwargs={'scale_grad_by_freq': True},)

        # gradcheck not implemented for sparse tensors.
        idx = make_long_input((2, 2), low=0, high=S)
        weights = make_input((S, S))
        yield SampleInput(weights, args=(idx,), kwargs={'sparse': True})

        idx = make_long_input((3, 3), low=0, high=S)
        idx[0, 0] = 1  # freq more than 1
        idx[0, 1] = 1  # freq more than 1
        idx[1, 0] = 0  # padding_idx
        weights = make_input((S, S)) * 2
        yield SampleInput(weights, args=(idx,),
                          kwargs={'sparse': True, 'scale_grad_by_freq': True,
                                  'padding_idx': 0, 'max_norm': 1.})

