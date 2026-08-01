
def error_inputs_median(op_info, device, **kwargs):
    x = torch.tensor([[[[[[[[[[[[[[[[[[[[[[[[[nan],
                               [nan]]]]]]]]]]]]]]]]]]]]]]]]], device=device)
    if device == 'cuda':
        yield ErrorInput(SampleInput(x, kwargs=dict(dim=(-1))),
                         error_type=RuntimeError,
                         error_regex='CUDA Tensors cannot have more than 25 dimensions')
    else:
        return

