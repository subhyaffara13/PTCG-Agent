
def is_fx_tracing_warning() -> None:
    log.warning(
        "is_fx_tracing will return true for both fx.symbolic_trace and "
        "torch.export. Please use "
        "is_fx_tracing_symbolic_tracing() for specifically fx.symbolic_trace "
        "or torch.compiler.is_compiling() for specifically torch.export/compile."
    )

