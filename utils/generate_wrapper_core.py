
def generate_wrapper_core(
    fn: FuncIR,
    emitter: Emitter,
    optional_args: list[RuntimeArg] | None = None,
    arg_names: list[str] | None = None,
    cleanups: list[str] | None = None,
    traceback_code: str | None = None,
) -> None:
    """Generates the core part of a wrapper function for a native function.

    This expects each argument as a PyObject * named obj_{arg} as a precondition.
    It converts the PyObject *s to the necessary types, checking and unboxing if necessary,
    makes the call, then boxes the result if necessary and returns it.
    """
    gen = WrapperGenerator(None, emitter)
    gen.set_target(fn)
    if arg_names:
        gen.arg_names = arg_names
    gen.cleanups = cleanups or []
    gen.optional_args = optional_args or []
    gen.traceback_code = traceback_code or ""

    error = ReturnHandler("NULL") if not gen.use_goto() else GotoHandler("fail")
    gen.emit_arg_processing(error=error)
    gen.emit_call()
    gen.emit_error_handling()

