
def sample_inputs_like_fns(self, device, dtype, requires_grad, **kwargs):
    inputs = [
        ((), {}),
        ((S, S), {}),
        ((0, S, 0), {}),
        ((S,), {'dtype': dtype, 'device': device}),
        # Hard-code some dtypes/devices. We want to test cases where the
        # (dtype, device) is different from the input's (dtype, device)
        ((S,), {'dtype': highest_precision_float(device)}),
        ((S,), {'device': 'cpu'}),
        ((S,), {'dtype': torch.double, 'device': 'cpu'}),
    ]
    if torch.cuda.is_available():
        inputs.append(((S,), {'device': 'cuda'}))

    for shape, kwargs in inputs:
        t = make_tensor(shape, dtype=dtype, device=device,
                        low=None, high=None,
                        requires_grad=requires_grad)
        yield SampleInput(t, **kwargs)

