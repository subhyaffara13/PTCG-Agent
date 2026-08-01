
def add_close_to_generator_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    """Generates the '__close__' method for a generator class."""
    with builder.enter_method(fn_info.generator_class.ir, "close", object_rprimitive, fn_info):
        except_block, else_block = BasicBlock(), BasicBlock()
        builder.builder.push_error_handler(except_block)
        builder.goto_and_activate(BasicBlock())
        generator_exit = builder.load_module_attr_by_fullname(
            "builtins.GeneratorExit", fn_info.fitem.line
        )
        builder.add(
            MethodCall(
                builder.self(),
                "throw",
                [generator_exit, builder.none_object(), builder.none_object()],
                fn_info.fitem.line,
            )
        )
        builder.goto(else_block)
        builder.builder.pop_error_handler()

        builder.activate_block(except_block)
        old_exc = builder.call_c(error_catch_op, [], fn_info.fitem.line)
        builder.nonlocal_control.append(
            ExceptNonlocalControl(builder.nonlocal_control[-1], old_exc)
        )
        stop_iteration = builder.load_module_attr_by_fullname(
            "builtins.StopIteration", fn_info.fitem.line
        )
        exceptions = builder.add(TupleSet([generator_exit, stop_iteration], fn_info.fitem.line))
        matches = builder.call_c(exc_matches_op, [exceptions], fn_info.fitem.line)

        match_block, non_match_block = BasicBlock(), BasicBlock()
        builder.add(Branch(matches, match_block, non_match_block, Branch.BOOL))

        builder.activate_block(match_block)
        builder.call_c(restore_exc_info_op, [builder.read(old_exc)], fn_info.fitem.line)
        builder.add(Return(builder.none_object()))

        builder.activate_block(non_match_block)
        builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
        builder.add(Unreachable())

        builder.nonlocal_control.pop()

        builder.activate_block(else_block)
        builder.add(
            RaiseStandardError(
                RaiseStandardError.RUNTIME_ERROR,
                "generator ignored GeneratorExit",
                fn_info.fitem.line,
            )
        )
        builder.add(Unreachable())

