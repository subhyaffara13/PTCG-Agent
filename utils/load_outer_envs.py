
def load_outer_envs(builder: IRBuilder, base: ImplicitClass) -> None:
    index = len(builder.builders) - 2

    # Load the first outer environment. This one is special because it gets saved in the
    # FuncInfo instance's prev_env_reg field.
    has_outer = index > 1 or (index == 1 and builder.fn_infos[1].contains_nested)
    if has_outer and builder.fn_infos[index]._env_class is not None:
        # outer_env = builder.fn_infos[index].environment
        outer_env = builder.symtables[index]
        if isinstance(base, GeneratorClass):
            base.prev_env_reg = load_outer_env(builder, base.curr_env_reg, outer_env)
        else:
            base.prev_env_reg = load_outer_env(builder, base.self_reg, outer_env)
        env_reg = base.prev_env_reg
        index -= 1

    # Load the remaining outer environments into registers.
    while index > 1:
        if builder.fn_infos[index]._env_class is None:
            break
        # outer_env = builder.fn_infos[index].environment
        outer_env = builder.symtables[index]
        env_reg = load_outer_env(builder, env_reg, outer_env)
        index -= 1

