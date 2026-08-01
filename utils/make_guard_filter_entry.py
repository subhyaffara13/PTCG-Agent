
def make_guard_filter_entry(guard: Guard, builder: GuardBuilder) -> GuardFilterEntry:
    MISSING = object()
    name = strip_local_scope(guard.name)
    if name == "":
        has_value = False
        value = MISSING
    else:
        try:
            # Guard evaluation is expected to fail when we guard on
            # things like "not hasattr(x, 'foo')". In cases like this,
            # we don't have a well defined value because such thing
            # doesn't exist.
            value = builder.get(guard)
            has_value = True
        except:  # noqa: B001,E722
            value = MISSING
            has_value = False
    is_global = get_global_source_name(guard.originating_source) is not None
    return GuardFilterEntry(
        name=name,
        has_value=has_value,
        value=value,
        guard_type=guard.create_fn_name(),
        derived_guard_types=(tuple(guard.guard_types) if guard.guard_types else ()),
        is_global=is_global,
        orig_guard=guard,
    )

