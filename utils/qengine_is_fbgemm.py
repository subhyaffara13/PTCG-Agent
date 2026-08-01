
def qengine_is_fbgemm():
    return torch.backends.quantized.engine == 'fbgemm'

