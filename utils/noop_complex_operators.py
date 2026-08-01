
def noop_complex_operators(g: jit_utils.GraphContext, input: _C.Value):
    # ONNX does not have operators to *directly* manipulate real/imaginary components
    # However, a few torch APIs (e.g. .tolist()) use complex operations when input is real,
    # which results in failures due to missing operators for complex numbers

    # `aten::resolve_conj` and `aten::resolve_neg` can safely be implemented as no-op
    return input

