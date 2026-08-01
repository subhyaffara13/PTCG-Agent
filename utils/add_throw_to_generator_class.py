
def add_throw_to_generator_class(builder: IRBuilder, fn_info: FuncInfo, fn_decl: FuncDecl) -> None:
    """Generates the 'throw' method for a generator class."""
    with builder.enter_method(fn_info.generator_class.ir, "throw", object_rprimitive, fn_info):
        typ = builder.add_argument("type", object_rprimitive)
        val = builder.add_argument("value", object_rprimitive, ARG_OPT)
        tb = builder.add_argument("traceback", object_rprimitive, ARG_OPT)

        # Because the value and traceback arguments are optional and hence
        # can be NULL if not passed in, we have to assign them Py_None if
        # they are not passed in.
        none_reg = builder.none_object()
        builder.assign_if_null(val, lambda: none_reg, fn_info.fitem.line)
        builder.assign_if_null(tb, lambda: none_reg, fn_info.fitem.line)

        # Call the helper function using the arguments passed in, and return that result.
        result = builder.add(
            Call(
                fn_decl,
                [
                    builder.self(),
                    builder.read(typ),
                    builder.read(val),
                    builder.read(tb),
                    none_reg,
                    Integer(0, object_pointer_rprimitive),
                ],
                fn_info.fitem.line,
            )
        )
        builder.add(Return(result))

