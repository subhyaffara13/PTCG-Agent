
def sample_inputs_corrcoef(op_info, device, dtype, requires_grad, **kwargs):
    return (SampleInput(t) for t in _generate_correlation_inputs(device, dtype, requires_grad))

