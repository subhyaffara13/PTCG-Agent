
def finalize_env_class(builder: IRBuilder, prefix: str = "") -> None:
    """Generate, instantiate, and set up the environment of an environment class."""
    if not builder.fn_info.can_merge_generator_and_env_classes():
        instantiate_env_class(builder)

    # Iterate through the function arguments and replace local definitions (using registers)
    # that were previously added to the environment with references to the function's
    # environment class. Comprehension scopes have no arguments to add.
    if not builder.fn_info.is_comprehension_scope:
        if builder.fn_info.is_nested:
            add_args_to_env(
                builder, local=False, base=builder.fn_info.callable_class, prefix=prefix
            )
        else:
            add_args_to_env(builder, local=False, base=builder.fn_info, prefix=prefix)

