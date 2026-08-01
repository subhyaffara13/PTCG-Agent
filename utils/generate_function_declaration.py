
def generate_function_declaration(fn: FuncIR, emitter: Emitter) -> None:
    emitter.context.declarations[emitter.native_function_name(fn.decl)] = HeaderDeclaration(
        f"{native_function_header(fn.decl, emitter)};", needs_export=True
    )
    if fn.name != TOP_LEVEL_NAME and not fn.internal:
        # needs_export=True so Python-wrapper (CPyPy_) symbols are reachable from
        # other groups via the export table — needed for cross-group inherited
        # __init__ / __new__ slot dispatch under `separate=True`.
        if is_fastcall_supported(fn, emitter.capi_version):
            emitter.context.declarations[PREFIX + fn.cname(emitter.names)] = HeaderDeclaration(
                f"{wrapper_function_header(fn, emitter.names)};", needs_export=True
            )
        else:
            emitter.context.declarations[PREFIX + fn.cname(emitter.names)] = HeaderDeclaration(
                f"{legacy_wrapper_function_header(fn, emitter.names)};", needs_export=True
            )

