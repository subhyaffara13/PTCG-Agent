from typing import Callable

def gen_generator_func(
    builder: IRBuilder,
    gen_func_ir: Callable[
        [list[Register], list[BasicBlock], FuncInfo], tuple[FuncIR, Value | None]
    ],
) -> tuple[FuncIR, Value | None]:
    """Generate IR for generator function that returns generator object."""
    setup_generator_class(builder)
    load_env_registers(builder, prefix=GENERATOR_ATTRIBUTE_PREFIX)
    gen_arg_defaults(builder)
    if builder.fn_info.can_merge_generator_and_env_classes():
        gen = instantiate_generator_class(builder)
        builder.fn_info._curr_env_reg = gen
        finalize_env_class(builder, prefix=GENERATOR_ATTRIBUTE_PREFIX)
    else:
        finalize_env_class(builder, prefix=GENERATOR_ATTRIBUTE_PREFIX)
        gen = instantiate_generator_class(builder)
    builder.add(Return(gen))

    args, _, blocks, ret_type, fn_info = builder.leave()
    func_ir, func_reg = gen_func_ir(args, blocks, fn_info)
    return func_ir, func_reg

