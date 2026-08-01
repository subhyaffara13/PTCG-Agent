
def _register_quantization_lowerings():
    _register_quantization_unary_lowering()
    _register_quantization_binary_lowering()
    _register_quantization_maxpool2d()
    _register_quantization_cat()
    _register_quantization_reshape()

