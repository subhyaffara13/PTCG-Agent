
def reference_layer_norm(inp: npt.NDArray, normalized_shape: tuple[int, ...], weight=None, bias=None, eps=1e-5):
    return reference_native_layer_norm(inp, normalized_shape, weight, bias, eps)[0]

