
def generate_traceback_code(
    fn: FuncIR, emitter: Emitter, source_path: str, module_name: str
) -> str:
    # If we hit an error while processing arguments, then we emit a
    # traceback frame to make it possible to debug where it happened.
    # Unlike traceback frames added for exceptions seen in IR, we do this
    # even if there is no `traceback_name`. This is because the error will
    # have originated here and so we need it in the traceback.
    globals_static = emitter.static_name("globals", module_name)
    traceback_code = 'CPy_AddTraceback("%s", "%s", %d, %s);' % (
        source_path.replace("\\", "\\\\"),
        fn.traceback_name or fn.name,
        fn.line,
        globals_static,
    )
    return traceback_code

