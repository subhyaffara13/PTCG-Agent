
def instantiate_env_class(builder: IRBuilder) -> Value:
    """Assign an environment class to a register named after the given function definition."""
    curr_env_reg = builder.add(
        Call(builder.fn_info.env_class.ctor, [], builder.fn_info.fitem.line)
    )

    if builder.fn_info.is_nested and not builder.fn_info.is_comprehension_scope:
        builder.fn_info.callable_class._curr_env_reg = curr_env_reg
        builder.add(
            SetAttr(
                curr_env_reg,
                ENV_ATTR_NAME,
                builder.fn_info.callable_class.prev_env_reg,
                builder.fn_info.fitem.line,
            )
        )
    else:
        # Top-level functions and comprehension scopes store env reg directly.
        builder.fn_info._curr_env_reg = curr_env_reg
        # Comprehension scopes link to parent env if it exists.
        if (
            builder.fn_info.is_nested
            and builder.fn_infos[-2]._env_class is not None
            and builder.fn_infos[-2]._curr_env_reg is not None
        ):
            builder.add(
                SetAttr(
                    curr_env_reg,
                    ENV_ATTR_NAME,
                    builder.fn_infos[-2].curr_env_reg,
                    builder.fn_info.fitem.line,
                )
            )

    return curr_env_reg

