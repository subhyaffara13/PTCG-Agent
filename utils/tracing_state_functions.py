
def tracing_state_functions() -> dict[Callable[[], Any], bool | None]:
    # Defined as a function to avoid circular import like torch.onnx
    return {
        torch.jit.is_scripting: False,
        torch.jit.is_tracing: False,
        torch._C._get_tracing_state: None,
        torch.fx._symbolic_trace.is_fx_tracing: False,
        torch.fx._symbolic_trace.is_fx_symbolic_tracing: False,
        torch.onnx.is_in_onnx_export: False,
        # pyrefly: ignore [deprecated]
        torch._dynamo.external_utils.is_compiling: True,
        # pyrefly: ignore [deprecated]
        torch._utils.is_compiling: True,
        torch.compiler.is_compiling: True,
        torch.compiler.is_dynamo_compiling: True,
        torch.compiler.is_exporting: True,
        torch._dynamo.eval_frame._is_in_optimized_module: True,
        # Look into https://github.com/pytorch/pytorch/pull/164721 why this is
        # turned to True for Dynamo.
        torch.nn.modules.activation._is_make_fx_tracing: True,
    }

