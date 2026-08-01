
def unsupported_output_tensor(t: torch.Tensor, node=None):
    "Do not support writing tensor but can read from it"
    supported_complex_views = (
        aten.view.dtype,
        torch.ops.prims.convert_element_type.default,
    )
    if node is not None and node.target in supported_complex_views and t.is_complex():
        return False
    if unsupported_input_tensor(t, node):
        return True
    return t.is_cpu and config.disable_cpp_codegen

