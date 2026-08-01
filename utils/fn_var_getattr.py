
def fn_var_getattr(
    tx: "InstructionTranslator", fn: object, source: Source | None, name: str
) -> VariableTracker:
    source = source and AttrSource(source, name)

    if source and name == "__annotations__":
        # We get a large number of silly guards from annotations from inspect
        # module. Changing annotations is rare, and it impacting the extracted
        # graph is even rarer. So skip guards.
        source = SkipGuardSource(source)

    subobj = None
    try:
        subobj = inspect.getattr_static(fn, name)
    except AttributeError:
        # function does not have a __getattr__ or __getattribute__ method,
        # so we can safely assume that this attribute is absent
        raise_observed_exception(AttributeError, tx)

    # Special handling for known dunder attributes
    # TODO(guilhermeleobas): this check should go through fn.__dict__ first as
    # functools.partial can override it
    if name in fn_known_dunder_attrs:
        subobj = getattr(fn, name)
    if source:
        return variables.LazyVariableTracker.create(subobj, source)
    return VariableTracker.build(tx, subobj)

