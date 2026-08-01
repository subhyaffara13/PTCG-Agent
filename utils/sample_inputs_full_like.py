
def sample_inputs_full_like(self, device, dtype, requires_grad, **kwargs):
    def get_val(dtype):
        return make_tensor([], dtype=dtype, device="cpu").item()

    double_dtype = highest_precision_float(device)
    inputs = [
        ((), get_val(dtype), {}),
        ((S, S), get_val(dtype), {}),
        ((0, S, 0), get_val(dtype), {}),
        ((S,), get_val(dtype), {'dtype': dtype, 'device': device}),
        # Hard-code some dtypes/devices. We want to test cases where the
        # (dtype, device) is different from the input's (dtype, device)
        ((S,), get_val(double_dtype), {'dtype': double_dtype}),
        ((S,), get_val(dtype), {'device': 'cpu'}),
        ((S,), get_val(double_dtype), {'dtype': double_dtype, 'device': 'cpu'}),
    ]
    if torch.cuda.is_available():
        inputs.append(((S,), get_val(dtype), {'device': 'cuda'}))

    if torch.mps.is_available() and dtype not in [torch.float64, torch.complex128, torch.uint32, torch.uint16]:
        inputs.append(((S,), get_val(dtype), {'device': 'mps'}))

    if not dtype.is_signed:
        # For unsigned dtypes, negative values are converted.
        inputs.append(((S,), -get_val(dtype), {}))

    for shape, fill_value, kwargs in inputs:
        t = make_tensor(shape, dtype=dtype, device=device,
                        low=None, high=None,
                        requires_grad=requires_grad)
        yield SampleInput(t, fill_value, **kwargs)

