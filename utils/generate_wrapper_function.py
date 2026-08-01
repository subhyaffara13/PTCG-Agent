
def generate_wrapper_function(
    fn: FuncIR, emitter: Emitter, source_path: str, module_name: str
) -> None:
    """Generate a CPython-compatible vectorcall wrapper for a native function.

    In particular, this handles unboxing the arguments, calling the native function, and
    then boxing the return value.
    """
    emitter.emit_line(f"{wrapper_function_header(fn, emitter.names)} {{")

    # If fn is a method, then the first argument is a self param
    real_args = list(fn.args)
    if fn.sig.num_bitmap_args:
        real_args = real_args[: -fn.sig.num_bitmap_args]
    if fn.class_name and fn.decl.kind != FUNC_STATICMETHOD:
        arg = real_args.pop(0)
        emitter.emit_line(f"PyObject *obj_{arg.name} = self;")

    # Need to order args as: required, optional, kwonly optional, kwonly required
    # This is because CPyArg_ParseStackAndKeywords format string requires
    # them grouped in that way.
    groups = make_arg_groups(real_args)
    reordered_args = reorder_arg_groups(groups)

    emitter.emit_line(make_static_kwlist(reordered_args))
    fmt = make_format_string(fn.name, groups)
    # Define the arguments the function accepts (but no types yet)
    emitter.emit_line(f'static CPyArg_Parser parser = {{"{fmt}", kwlist, 0}};')

    for arg in real_args:
        emitter.emit_line(
            "PyObject *obj_{}{};".format(arg.name, " = NULL" if arg.optional else "")
        )

    cleanups = [f"CPy_DECREF(obj_{arg.name});" for arg in groups[ARG_STAR] + groups[ARG_STAR2]]

    arg_ptrs: list[str] = []
    if groups[ARG_STAR] or groups[ARG_STAR2]:
        arg_ptrs += [f"&obj_{groups[ARG_STAR][0].name}" if groups[ARG_STAR] else "NULL"]
        arg_ptrs += [f"&obj_{groups[ARG_STAR2][0].name}" if groups[ARG_STAR2] else "NULL"]
    arg_ptrs += [f"&obj_{arg.name}" for arg in reordered_args]

    if fn.name == "__call__":
        nargs = "PyVectorcall_NARGS(nargs)"
    else:
        nargs = "nargs"
    parse_fn = "CPyArg_ParseStackAndKeywords"
    # Special case some common signatures
    if not real_args:
        # No args
        parse_fn = "CPyArg_ParseStackAndKeywordsNoArgs"
    elif len(real_args) == 1 and len(groups[ARG_POS]) == 1:
        # Single positional arg
        parse_fn = "CPyArg_ParseStackAndKeywordsOneArg"
    elif len(real_args) == len(groups[ARG_POS]) + len(groups[ARG_OPT]):
        # No keyword-only args, *args or **kwargs
        parse_fn = "CPyArg_ParseStackAndKeywordsSimple"
    emitter.emit_lines(
        "if (!{}(args, {}, kwnames, &parser{})) {{".format(
            parse_fn, nargs, "".join(", " + n for n in arg_ptrs)
        ),
        "return NULL;",
        "}",
    )
    for i in range(fn.sig.num_bitmap_args):
        name = bitmap_name(i)
        emitter.emit_line(f"{BITMAP_TYPE} {name} = 0;")
    traceback_code = generate_traceback_code(fn, emitter, source_path, module_name)
    generate_wrapper_core(
        fn,
        emitter,
        groups[ARG_OPT] + groups[ARG_NAMED_OPT],
        cleanups=cleanups,
        traceback_code=traceback_code,
    )

    emitter.emit_line("}")

