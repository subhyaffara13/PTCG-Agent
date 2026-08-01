
def gen_glue_method(
    builder: IRBuilder,
    base_sig: FuncSignature,
    target: FuncIR,
    cls: ClassIR,
    base: ClassIR,
    line: int,
    do_pycall: bool,
) -> FuncIR:
    """Generate glue methods that mediate between different method types in subclasses.

    For example, if we have:

    class A:
        def f(builder: IRBuilder, x: int) -> object: ...

    then it is totally permissible to have a subclass

    class B(A):
        def f(builder: IRBuilder, x: object) -> int: ...

    since '(object) -> int' is a subtype of '(int) -> object' by the usual
    contra/co-variant function subtyping rules.

    The trickiness here is that int and object have different
    runtime representations in mypyc, so A.f and B.f have
    different signatures at the native C level. To deal with this,
    we need to generate glue methods that mediate between the
    different versions by coercing the arguments and return
    values.

    If do_pycall is True, then make the call using the C API
    instead of a native call.
    """
    check_native_override(builder, base_sig, target.decl.sig, line)

    builder.enter()
    builder.ret_types[-1] = base_sig.ret_type

    rt_args = list(base_sig.args)
    if target.decl.kind == FUNC_NORMAL:
        rt_args[0] = RuntimeArg(base_sig.args[0].name, RInstance(cls))

    arg_info = get_args(builder, rt_args, line)
    args, arg_kinds, arg_names = arg_info.args, arg_info.arg_kinds, arg_info.arg_names

    bitmap_args = None
    if base_sig.num_bitmap_args:
        args = args[: -base_sig.num_bitmap_args]
        arg_kinds = arg_kinds[: -base_sig.num_bitmap_args]
        arg_names = arg_names[: -base_sig.num_bitmap_args]
        bitmap_args = list(builder.builder.args[-base_sig.num_bitmap_args :])

    # We can do a passthrough *args/**kwargs with a native call, but if the
    # args need to get distributed out to arguments, we just let python handle it
    if any(kind.is_star() for kind in arg_kinds) and any(
        not arg.kind.is_star() for arg in target.decl.sig.args
    ):
        do_pycall = True

    if do_pycall:
        if target.decl.kind == FUNC_STATICMETHOD:
            # FIXME: this won't work if we can do interpreted subclasses
            first = builder.builder.get_native_type(cls)
            st = 0
        else:
            first = args[0]
            st = 1
        retval = builder.builder.py_method_call(
            first, target.name, args[st:], line, arg_kinds[st:], arg_names[st:]
        )
    else:
        retval = builder.builder.call(
            target.decl, args, arg_kinds, arg_names, line, bitmap_args=bitmap_args
        )
    retval = builder.coerce(retval, base_sig.ret_type, line)
    builder.add(Return(retval))

    arg_regs, _, blocks, ret_type, _ = builder.leave()
    if base_sig.num_bitmap_args:
        rt_args = rt_args[: -base_sig.num_bitmap_args]
    return FuncIR(
        FuncDecl(
            target.name + "__" + base.name + "_glue",
            cls.name,
            builder.module_name,
            FuncSignature(rt_args, ret_type),
            target.decl.kind,
            is_coroutine=target.decl.is_coroutine,
        ),
        arg_regs,
        blocks,
    )

