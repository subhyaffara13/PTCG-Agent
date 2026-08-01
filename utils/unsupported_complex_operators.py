
def unsupported_complex_operators(g: jit_utils.GraphContext, input: _C.Value):
    # ONNX does not have operators to *directly* manipulate real/imaginary components
    # However, a few torch APIs (e.g. .tolist()) use complex operations when input is real,
    # which results in failures due to missing operators for complex numbers

    # While `aten::_conj` and `aten::conj_physical` raise exception when input is complex
    if symbolic_helper.is_complex_value(input):
        # FIXME(justinchuby): report correct name for symbolic being executed
        return symbolic_helper._onnx_unsupported(
            "aten::_conj, aten::conj_physical",
            input,
        )

    # they can safely be implemented as no-op for real numbers only
    return noop_complex_operators(g, input)

