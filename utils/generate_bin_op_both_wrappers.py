
def generate_bin_op_both_wrappers(
    cl: ClassIR, fn: FuncIR, fn_rev: FuncIR, emitter: Emitter, gen: WrapperGenerator
) -> None:
    # There's both a forward and a reverse operator method. First
    # check if we should try calling the forward one. If the
    # argument type check fails, fall back to the reverse method.
    #
    # Similar to above, we can't perfectly match Python semantics.
    # In regular Python code you'd return NotImplemented if the
    # operand has the wrong type, but in compiled code we'll never
    # get to execute the type check.
    emitter.emit_line(
        "if (PyObject_IsInstance(obj_left, (PyObject *){})) {{".format(
            emitter.type_struct_name(cl)
        )
    )
    gen.emit_arg_processing(error=GotoHandler("typefail"), raise_exception=False)
    handle_third_pow_argument(fn, emitter, gen, if_unsupported=["goto typefail2;"])
    # Ternary __rpow__ calls aren't a thing so immediately bail
    # if ternary __pow__ returns NotImplemented.
    if fn.name == "__pow__" and len(fn.args) == 3:
        fwd_not_implemented_handler = "goto typefail2;"
    else:
        fwd_not_implemented_handler = "goto typefail;"
    gen.emit_call(not_implemented_handler=fwd_not_implemented_handler)
    gen.emit_error_handling()
    emitter.emit_line("}")
    emitter.emit_label("typefail")
    emitter.emit_line(
        "if (PyObject_IsInstance(obj_right, (PyObject *){})) {{".format(
            emitter.type_struct_name(cl)
        )
    )
    gen.set_target(fn_rev)
    gen.arg_names = ["right", "left"]
    gen.emit_arg_processing(error=GotoHandler("typefail2"), raise_exception=False)
    handle_third_pow_argument(fn_rev, emitter, gen, if_unsupported=["goto typefail2;"])
    gen.emit_call()
    gen.emit_error_handling()
    emitter.emit_line("} else {")
    generate_bin_op_reverse_dunder_call(fn, emitter, fn_rev.name)
    emitter.emit_line("}")
    emitter.emit_label("typefail2")
    emitter.emit_line("Py_INCREF(Py_NotImplemented);")
    emitter.emit_line("return Py_NotImplemented;")
    gen.finish()

