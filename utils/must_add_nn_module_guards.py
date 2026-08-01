
def must_add_nn_module_guards(guard: Guard) -> bool:
    # For config.guard_nn_modules=False, we can skip all the guards that
    # originate from inside of nn module except for a few categories.
    return (
        # Guard for defaults
        isinstance(guard.originating_source, DefaultsSource)
        # Guard using dict tags if the config flag is set
        or (
            config.guard_nn_modules_using_dict_tags
            and guard.create_fn is GuardBuilder.NN_MODULE
        )
    )

