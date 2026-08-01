
def qengine_is_qnnpack():
    return torch.backends.quantized.engine == 'qnnpack'

