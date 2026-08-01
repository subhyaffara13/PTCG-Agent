
def gen_arg_defaults(builder: IRBuilder) -> None:
    """Generate blocks for arguments that have default values.

    If the passed value is an error value, then assign the default
    value to the argument.
    """
    fitem = builder.fn_info.fitem
    nb = 0
    for arg in fitem.arguments:
        if arg.initializer:
            target = builder.lookup(arg.variable)

            def get_default() -> Value:
                assert arg.initializer is not None

                # If it is constant, don't bother storing it
                if is_constant(arg.initializer):
                    return builder.accept(arg.initializer)

                # Because gen_arg_defaults runs before calculate_arg_defaults, we
                # add the static/attribute to final_names/the class here.
                elif not builder.fn_info.is_nested:
                    name = fitem.fullname + "." + arg.variable.name
                    builder.final_names.append((name, target.type))
                    return builder.add(LoadStatic(target.type, name, builder.module_name))
                else:
                    name = arg.variable.name
                    builder.fn_info.callable_class.ir.attributes[name] = target.type
                    return builder.add(
                        GetAttr(builder.fn_info.callable_class.self_reg, name, arg.line)
                    )

            assert isinstance(target, AssignmentTargetRegister), target
            reg = target.register
            if not reg.type.error_overlap:
                builder.assign_if_null(target.register, get_default, arg.initializer.line)
            else:
                builder.assign_if_bitmap_unset(
                    target.register, get_default, nb, arg.initializer.line
                )
                nb += 1

