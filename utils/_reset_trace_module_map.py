
def _reset_trace_module_map() -> None:
    torch.jit._trace._trace_module_map = None
    _C._jit_pass_onnx_clear_scope_records()

