
def create_generator_class_for_func(
    module_name: str, class_name: str | None, fdef: FuncDef, mapper: Mapper, name_suffix: str = ""
) -> ClassIR:
    """For a generator/async function, declare a generator class.

    Each generator and async function gets a dedicated class that implements the
    generator protocol with generated methods.
    """
    assert fdef.is_coroutine or fdef.is_generator
    name = "_".join(x for x in [fdef.name, class_name] if x) + "_gen" + name_suffix
    cir = ClassIR(name, module_name, is_generated=True, is_final_class=class_name is None)
    cir.reuse_freed_instance = True
    mapper.fdef_to_generator[fdef] = cir

    helper_sig = FuncSignature(
        (
            RuntimeArg(SELF_NAME, object_rprimitive),
            RuntimeArg("type", object_rprimitive),
            RuntimeArg("value", object_rprimitive),
            RuntimeArg("traceback", object_rprimitive),
            RuntimeArg("arg", object_rprimitive),
            # If non-NULL, used to store return value instead of raising StopIteration(retv)
            RuntimeArg("stop_iter_ptr", object_pointer_rprimitive),
        ),
        object_rprimitive,
    )

    # The implementation of most generator functionality is behind this magic method.
    helper_fn_decl = FuncDecl(GENERATOR_HELPER_NAME, name, module_name, helper_sig, internal=True)
    cir.method_decls[helper_fn_decl.name] = helper_fn_decl
    return cir

