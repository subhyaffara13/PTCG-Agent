
def compile_context(
    context: CompileContext | None,
) -> Generator[CompileContext | None, None, None]:
    old_context = getattr(_TLS, "compile_context", None)
    _TLS.compile_context = context
    try:
        yield context
    finally:
        _TLS.compile_context = old_context

