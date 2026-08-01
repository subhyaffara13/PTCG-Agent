
def add_next_to_generator_class(builder: IRBuilder, fn_info: FuncInfo, fn_decl: FuncDecl) -> None:
    """Generates the '__next__' method for a generator class."""
    with builder.enter_method(fn_info.generator_class.ir, "__next__", object_rprimitive, fn_info):
        none_reg = builder.none_object()
        # Call the helper function with error flags set to Py_None, and return that result.
        result = builder.add(
            Call(
                fn_decl,
                [
                    builder.self(),
                    none_reg,
                    none_reg,
                    none_reg,
                    none_reg,
                    Integer(0, object_pointer_rprimitive),
                ],
                fn_info.fitem.line,
            )
        )
        builder.add(Return(result))

