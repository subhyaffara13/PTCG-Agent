
def qengine_is_x86():
    return torch.backends.quantized.engine == 'x86'

