
def transform_with(
    builder: IRBuilder,
    expr: Expression,
    target: Lvalue | None,
    body: GenFunc,
    is_async: bool,
    line: int,
) -> None:
    # This is basically a straight transcription of the Python code in PEP 343.
    # I don't actually understand why a bunch of it is the way it is.
    # We could probably optimize the case where the manager is compiled by us,
    # but that is not our common case at all, so.

    al = "a" if is_async else ""

    mgr_v = builder.accept(expr)

    if not is_async and mgr_v.type == lock_rprimitive:
        transform_with_lock(builder, mgr_v, target, body, line)
        return
    is_native = isinstance(mgr_v.type, RInstance)
    if is_native:
        value = builder.add(MethodCall(mgr_v, f"__{al}enter__", args=[], line=line))
        exit_ = None
    else:
        typ = builder.primitive_op(type_op, [mgr_v], line)
        exit_ = builder.maybe_spill(builder.py_get_attr(typ, f"__{al}exit__", line))
        value = builder.py_call(builder.py_get_attr(typ, f"__{al}enter__", line), [mgr_v], line)

    mgr = builder.maybe_spill(mgr_v)
    exc = builder.maybe_spill_assignable(builder.true())
    if is_async:
        value = emit_await(builder, value, line)

    def maybe_natively_call_exit(exc_info: bool) -> Value:
        if exc_info:
            args = get_sys_exc_info(builder)
        else:
            none = builder.none_object()
            args = [none, none, none]

        if is_native:
            assert isinstance(mgr_v.type, RInstance), mgr_v.type
            exit_val = builder.gen_method_call(
                builder.read(mgr, line),
                f"__{al}exit__",
                arg_values=args,
                line=line,
                result_type=none_rprimitive,
            )
        else:
            assert exit_ is not None
            exit_val = builder.py_call(
                builder.read(exit_, line), [builder.read(mgr, line)] + args, line
            )

        if is_async:
            return emit_await(builder, exit_val, line)
        else:
            return exit_val

    def try_body() -> None:
        if target:
            builder.assign(builder.get_assignment_target(target), value, line)
        body()

    def except_body() -> None:
        builder.assign(exc, builder.false(), line)
        out_block, reraise_block = BasicBlock(), BasicBlock()
        builder.add_bool_branch(maybe_natively_call_exit(exc_info=True), out_block, reraise_block)
        builder.activate_block(reraise_block)
        builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
        builder.add(Unreachable())
        builder.activate_block(out_block)

    def finally_body() -> None:
        out_block, exit_block = BasicBlock(), BasicBlock()
        builder.add(Branch(builder.read(exc, line), exit_block, out_block, Branch.BOOL))
        builder.activate_block(exit_block)

        maybe_natively_call_exit(exc_info=False)
        builder.goto_and_activate(out_block)

    transform_try_finally_stmt(
        builder,
        lambda: transform_try_except(builder, try_body, [(None, None, except_body)], None, line),
        finally_body,
        line,
    )

