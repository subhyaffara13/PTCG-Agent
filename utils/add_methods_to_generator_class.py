
def add_methods_to_generator_class(
    builder: IRBuilder,
    fn_info: FuncInfo,
    arg_regs: list[Register],
    blocks: list[BasicBlock],
    is_coroutine: bool,
) -> None:
    helper_fn_decl = add_helper_to_generator_class(builder, arg_regs, blocks, fn_info)
    add_next_to_generator_class(builder, fn_info, helper_fn_decl)
    add_send_to_generator_class(builder, fn_info, helper_fn_decl)
    add_iter_to_generator_class(builder, fn_info)
    add_throw_to_generator_class(builder, fn_info, helper_fn_decl)
    add_close_to_generator_class(builder, fn_info)
    if is_coroutine:
        add_await_to_generator_class(builder, fn_info)

