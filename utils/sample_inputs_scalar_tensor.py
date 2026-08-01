
def sample_inputs_scalar_tensor(op, device, dtype, requires_grad, **kwargs):
    # Not including a scalar tensor in vals because meta tests start failing due to
    # lack of meta support for _local_scalar_dense
    # torch.tensor(2, device=device)
    vals = (-5, 0, 1)

    for item in vals:
        yield SampleInput(item, device=device, dtype=dtype, requires_grad=requires_grad)

