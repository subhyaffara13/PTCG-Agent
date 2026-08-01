
def wrap_backend_debug(
    unconfigured_compiler_fn: CompilerFn, compiler_name: str | None
) -> WrapBackendDebug:
    """
    A minifier decorator that wraps the TorchDynamo produced Fx graph modules.
    As opposed to wrap_compiler_debug, this wrapper intercepts at the
    TorchDynamo produced Fx Graph Module. This makes it backend-agnostic to some
    level, e.g., it is useful for minifying issues related to Aot Autograd
    tracing.  If an error is found, we minify and save the minified repro in
    repro.tar.gz.
    """
    return WrapBackendDebug(unconfigured_compiler_fn, compiler_name)

