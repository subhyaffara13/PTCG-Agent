
def adapt_inputs_to_device(sample_inputs: tuple, device: torch.device) -> tuple:
    """move inputs to device"""
    sample_inputs_ = []
    for sample_int in sample_inputs:
        if isinstance(sample_int, torch.Tensor):
            sample_inputs_.append(sample_int.to(device))
        else:
            sample_inputs_.append(sample_int)
    return tuple(sample_inputs_)

