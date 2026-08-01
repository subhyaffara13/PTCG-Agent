
def quantize_linear_modules(module, dtype=torch.int8):
    raise RuntimeError(
        "quantize_linear_modules function is no longer supported. "
        "Please use torch.ao.quantization.quantize_dynamic API instead."
    )

