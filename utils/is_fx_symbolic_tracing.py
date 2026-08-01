
def is_fx_symbolic_tracing() -> bool:
    return _is_fx_tracing_flag and not torch.compiler.is_compiling()

