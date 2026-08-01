
def check_self_arg(
    functype: FunctionLike,
    dispatched_arg_type: Type,
    is_classmethod: bool,
    context: Context,
    name: str,
    msg: MessageBuilder,
) -> FunctionLike:
    """Check that an instance has a valid type for a method with annotated 'self'.

    For example if the method is defined as:
        class A:
            def f(self: S) -> T: ...
    then for 'x.f' we check that type(x) <: S. If the method is overloaded, we select
    only overloads items that satisfy this requirement. If there are no matching
    overloads, an error is generated.
    """
    items = functype.items
    if not items:
        return functype
    new_items = []
    if is_classmethod:
        dispatched_arg_type = TypeType.make_normalized(dispatched_arg_type)
    p_dispatched_arg_type = get_proper_type(dispatched_arg_type)

    for item in items:
        if not item.arg_types or item.arg_kinds[0] not in (ARG_POS, ARG_STAR):
            # No positional first (self) argument (*args is okay).
            msg.no_formal_self(name, item, context)
            # This is pretty bad, so just return the original signature if
            # there is at least one such error.
            return functype
        selfarg = get_proper_type(item.arg_types[0])
        if isinstance(selfarg, Instance) and isinstance(p_dispatched_arg_type, Instance):
            if selfarg.type is p_dispatched_arg_type.type and selfarg.args:
                if not is_overlapping_types(p_dispatched_arg_type, selfarg):
                    # This special casing is needed since `actual <: erased(template)`
                    # logic below doesn't always work, and a more correct approach may
                    # be tricky.
                    continue
        new_items.append(item)

    if new_items:
        items = new_items
        new_items = []

    for item in items:
        selfarg = get_proper_type(item.arg_types[0])
        # This matches similar special-casing in bind_self(), see more details there.
        self_callable = name == "__call__" and isinstance(selfarg, CallableType)
        if self_callable or is_subtype(
            dispatched_arg_type,
            # This level of erasure matches the one in checker.check_func_def(),
            # better keep these two checks consistent.
            erase_typevars(erase_to_bound(selfarg)),
            # This is to work around the fact that erased ParamSpec and TypeVarTuple
            # callables are not always compatible with non-erased ones both ways.
            always_covariant=any(
                not isinstance(tv, TypeVarType) for tv in get_all_type_vars(selfarg)
            ),
            ignore_pos_arg_names=True,
        ):
            new_items.append(item)
        elif isinstance(selfarg, ParamSpecType):
            # TODO: This is not always right. What's the most reasonable thing to do here?
            new_items.append(item)
        elif isinstance(selfarg, TypeVarTupleType):
            raise NotImplementedError
    if not new_items:
        # Choose first item for the message (it may be not very helpful for overloads).
        msg.incompatible_self_argument(
            name, dispatched_arg_type, items[0], is_classmethod, context
        )
        return functype
    if len(new_items) == 1:
        return new_items[0]
    return Overloaded(new_items)

