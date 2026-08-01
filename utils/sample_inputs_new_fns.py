
def sample_inputs_new_fns(self, device, dtype, requires_grad, *, is_strided=False, **kwargs):
    # input_shape, output_shape, strides, kwargs
    # lengths of output_shape and strides must be equal
    inputs = [
        ((), (), (), {}),
        ((S, S), (2, 0), (3, 4), {}),
        ((0, S, 0), (3, 2, 2), (1, 2, 3), {}),
        ((S,), (2, 3), (7, 8), {'dtype': dtype, 'device': device}),
        # Hard-code some dtypes/devices. We want to test cases where the
        # (dtype, device) is different from the input's (dtype, device)
        ((S,), (10,), (S,), {'dtype': highest_precision_float(device)}),
        ((S,), (1, 1, 12), (S, L, M), {'device': 'cpu'}),
        ((S,), (2, 2, 2), (L, M, S), {'dtype': torch.double, 'device': 'cpu'}),
    ]
    if torch.cuda.is_available():
        inputs.append(((S,), (7, 2), (3, 4), {'device': 'cuda'}))

    for input_shape, output_shape, strides, kwargs in inputs:
        t = make_tensor(input_shape, dtype=dtype, device=device,
                        low=None, high=None,
                        requires_grad=requires_grad)
        if is_strided:
            yield SampleInput(t, output_shape, strides, **kwargs)
        else:
            yield SampleInput(t, output_shape, **kwargs)

