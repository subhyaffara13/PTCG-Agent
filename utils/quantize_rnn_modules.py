
def quantize_rnn_modules(module, dtype=torch.int8):
    raise RuntimeError(
        "quantize_rnn_modules function is no longer supported. "
        "Please use torch.ao.quantization.quantize_dynamic API instead."
    )

