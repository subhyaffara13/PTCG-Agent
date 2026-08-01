
def emit_yield_from_or_await(
    builder: IRBuilder, val: Value, line: int, *, is_await: bool
) -> Value:
    # This is basically an implementation of the code in PEP 380.

    # TODO: do we want to use the right types here?
    result = Register(object_rprimitive, line=line)
    to_yield_reg = Register(object_rprimitive, line=line)
    received_reg = Register(object_rprimitive, line=line)

    helper_method = GENERATOR_HELPER_NAME
    if (
        isinstance(val, (Call, MethodCall))
        and isinstance(val.type, RInstance)
        and val.type.class_ir.has_method(helper_method)
    ):
        # This is a generated native generator class, and we can use a fast path.
        # This allows two optimizations:
        # 1) No need to call CPy_GetCoro() or iter() since for native generators
        #    it just returns the generator object (implemented here).
        # 2) Instead of calling next(), call generator helper method directly,
        #    since next() just calls __next__ which calls the helper method.
        iter_val: Value = val
    else:
        get_op = coro_op if is_await else iter_op
        if isinstance(get_op, PrimitiveDescription):
            iter_val = builder.primitive_op(get_op, [val], line)
        else:
            iter_val = builder.call_c(get_op, [val], line)

    iter_reg = builder.maybe_spill_assignable(iter_val)

    stop_block, main_block, done_block = BasicBlock(), BasicBlock(), BasicBlock()

    if isinstance(iter_reg.type, RInstance) and iter_reg.type.class_ir.has_method(helper_method):
        # Second fast path optimization: call helper directly (see also comment above).
        #
        # Calling a generated generator, so avoid raising StopIteration by passing
        # an extra PyObject ** argument to helper where the stop iteration value is stored.
        fast_path = True
        obj = builder.read(iter_reg, line)
        nn = builder.none_object()
        stop_iter_val = Register(object_rprimitive)
        err = builder.add(LoadErrorValue(object_rprimitive, undefines=True))
        builder.assign(stop_iter_val, err, line)
        ptr = builder.add(LoadAddress(object_pointer_rprimitive, stop_iter_val))
        m = MethodCall(obj, helper_method, [nn, nn, nn, nn, ptr], line)
        # Generators have custom error handling, so disable normal error handling.
        m.error_kind = ERR_NEVER
        _y_init = builder.add(m)
    else:
        fast_path = False
        _y_init = builder.call_c(next_raw_op, [builder.read(iter_reg, line)], line)

    builder.add(Branch(_y_init, stop_block, main_block, Branch.IS_ERROR))

    builder.activate_block(stop_block)
    if fast_path:
        builder.primitive_op(propagate_if_error_op, [stop_iter_val], line)
        builder.assign(result, stop_iter_val, line)
    else:
        # Try extracting a return value from a StopIteration and return it.
        # If it wasn't, this reraises the exception.
        builder.assign(result, builder.call_c(check_stop_op, [], line), line)
    # Clear the spilled iterator/coroutine so that it will be freed.
    # Otherwise, the freeing of the spilled register would likely be delayed.
    err = builder.add(LoadErrorValue(iter_reg.type))
    builder.assign(iter_reg, err, line)
    builder.goto(done_block)

    builder.activate_block(main_block)
    builder.assign(to_yield_reg, _y_init, line)

    # OK Now the main loop!
    loop_block = BasicBlock()
    builder.goto_and_activate(loop_block)

    def try_body() -> None:
        builder.assign(
            received_reg, emit_yield(builder, builder.read(to_yield_reg, line), line), line
        )

    def except_body() -> None:
        # The body of the except is all implemented in a C function to
        # reduce how much code we need to generate. It returns a value
        # indicating whether to break or yield (or raise an exception).
        val = Register(object_rprimitive)
        val_address = builder.add(LoadAddress(object_pointer_rprimitive, val))
        to_stop = builder.call_c(
            yield_from_except_op, [builder.read(iter_reg, line), val_address], line
        )

        ok, stop = BasicBlock(), BasicBlock()
        builder.add(Branch(to_stop, stop, ok, Branch.BOOL))

        # The exception got swallowed. Continue, yielding the returned value
        builder.activate_block(ok)
        builder.assign(to_yield_reg, val, line)
        builder.nonlocal_control[-1].gen_continue(builder, line)

        # The exception was a StopIteration. Stop iterating.
        builder.activate_block(stop)
        builder.assign(result, val, line)
        builder.nonlocal_control[-1].gen_break(builder, line)

    def else_body() -> None:
        # Do a next() or a .send(). It will return NULL on exception
        # but it won't automatically propagate.
        _y = builder.call_c(
            send_op, [builder.read(iter_reg, line), builder.read(received_reg, line)], line
        )
        ok, stop = BasicBlock(), BasicBlock()
        builder.add(Branch(_y, stop, ok, Branch.IS_ERROR))

        # Everything's fine. Yield it.
        builder.activate_block(ok)
        builder.assign(to_yield_reg, _y, line)
        builder.nonlocal_control[-1].gen_continue(builder, line)

        # Try extracting a return value from a StopIteration and return it.
        # If it wasn't, this rereaises the exception.
        builder.activate_block(stop)
        builder.assign(result, builder.call_c(check_stop_op, [], line), line)
        builder.nonlocal_control[-1].gen_break(builder, line)

    builder.push_loop_stack(loop_block, done_block)
    transform_try_except(builder, try_body, [(None, None, except_body)], else_body, line)
    builder.pop_loop_stack()

    builder.goto_and_activate(done_block)
    return builder.read(result, line)

