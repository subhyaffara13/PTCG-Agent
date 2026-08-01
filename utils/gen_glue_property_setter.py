
def gen_glue_property_setter(
    builder: IRBuilder, sig: FuncSignature, target: FuncIR, cls: ClassIR, base: ClassIR, line: int
) -> FuncIR:
    """Generate a shadow glue method for a property setter.

    For interpreted subclasses, property setters can't be called via the
    internal __mypyc_setter__<name> method. Instead, use Python's setattr
    to set the property via the standard descriptor protocol.
    """
    builder.enter()
    builder.ret_types[-1] = sig.ret_type

    rt_args = list(sig.args)
    rt_args[0] = RuntimeArg(sig.args[0].name, RInstance(cls))

    arg_info = get_args(builder, rt_args, line)
    args = arg_info.args

    self_arg = args[0]
    value_arg = args[1]

    # Extract the property name from "__mypyc_setter__<name>"
    assert target.name.startswith(PROPSET_PREFIX)
    prop_name = target.name[len(PROPSET_PREFIX) :]

    builder.primitive_op(
        py_setattr_op,
        [
            self_arg,
            builder.load_str(prop_name),
            builder.coerce(value_arg, object_rprimitive, line),
        ],
        line,
    )
    retval = builder.coerce(builder.none(), sig.ret_type, line)
    builder.add(Return(retval))

    arg_regs, _, blocks, return_type, _ = builder.leave()
    return FuncIR(
        FuncDecl(
            target.name + "__" + base.name + "_glue",
            cls.name,
            builder.module_name,
            FuncSignature(rt_args, return_type),
        ),
        arg_regs,
        blocks,
    )

