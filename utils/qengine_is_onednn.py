
def qengine_is_onednn():
    return torch.backends.quantized.engine == 'onednn'

