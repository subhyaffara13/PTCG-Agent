
def error_inputs_prelu(op, device):
    # Weight has numel != 1, but self.ndim is zero-dim tensor
    inp = make_tensor((), device=device, dtype=torch.float32)
    weight = make_tensor((2,), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(inp, kwargs={'weight': weight}),
                     error_regex="Not allow zero-dim input tensor.")

    # Weight has numel != 1, but numel does not match channel size
    inp = make_tensor((2, 8, 3), device=device, dtype=torch.float32)
    weight = make_tensor((9,), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(inp, kwargs={'weight': weight}),
                     error_regex="Mismatch of parameter numbers and input channel size.")

    # Weight is neither a scalar nor 1-D tensor
    inp = make_tensor((2, 8, 3), device=device, dtype=torch.float32)
    weight = make_tensor((2, 4), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(inp, kwargs={'weight': weight}),
                     error_regex="prelu: Expected `weight` to be a scalar or 1D tensor, but got: ndim = 2")

