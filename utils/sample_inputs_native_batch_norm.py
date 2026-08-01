
def sample_inputs_native_batch_norm(op_info, device, dtype, requires_grad, **kwargs):
    samples = sample_inputs_batch_norm(op_info, device, dtype, requires_grad, **kwargs)
    for sample in samples:
        # torch.native_batch_norm does not support 0 numel tensors
        # IndexError: Dimension out of range (expected to be in range of [-1, 0], but got 1)
        if sample.input.numel() == 0:
            continue
        args = sample.args
        training = sample.kwargs.get('training', True)
        momentum = sample.kwargs.get('momentum', 0.5)
        eps = sample.kwargs.get('eps', 1e-5)
        yield SampleInput(sample.input, args=(args[2], args[3], args[0], args[1], training, momentum, eps))

