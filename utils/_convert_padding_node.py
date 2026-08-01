
def _convert_padding_node(input):
    padding = symbolic_helper._maybe_get_const(input, "is")
    if symbolic_helper._is_value(padding) and symbolic_helper._is_packed_list(padding):
        input_list = symbolic_helper._unpack_list(padding)
        try:
            padding = [
                symbolic_helper._get_const(v, "i", "padding") for v in input_list
            ]
        except Exception:
            # FIXME(justinchuby): Avoid catching Exception.
            # Catch a more specific exception instead.
            return symbolic_helper._onnx_opset_unsupported_detailed(
                "Pad", 9, 11, "The sizes of the padding must be constant", input
            )
    return padding

