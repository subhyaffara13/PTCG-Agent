
def gen_glue_property(
    builder: IRBuilder,
    sig: FuncSignature,
    target: FuncIR,
    cls: ClassIR,
    base: ClassIR,
    line: int,
    do_pygetattr: bool,
) -> FuncIR:
    """Generate glue methods for properties that mediate between different subclass types.

    Similarly to methods, properties of derived types can be covariantly subtyped. Thus,
    properties also require glue. However, this only requires the return type to change.
    Further, instead of a method call, an attribute get is performed.

    If do_pygetattr is True, then get the attribute using the Python C
    API instead of a native call.
    """
    builder.enter()

    rt_arg = RuntimeArg(SELF_NAME, RInstance(cls))
    self_target = builder.add_self_to_env(cls)
    arg = builder.read(self_target, line)
    builder.ret_types[-1] = sig.ret_type
    if do_pygetattr:
        retval = builder.py_get_attr(arg, target.name, line)
    else:
        retval = builder.add(GetAttr(arg, target.name, line))
    retbox = builder.coerce(retval, sig.ret_type, line)
    builder.add(Return(retbox))

    args, _, blocks, return_type, _ = builder.leave()
    return FuncIR(
        FuncDecl(
            target.name + "__" + base.name + "_glue",
            cls.name,
            builder.module_name,
            FuncSignature([rt_arg], return_type),
        ),
        args,
        blocks,
    )

