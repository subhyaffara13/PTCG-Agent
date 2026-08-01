
def attr_class_maker_callback_impl(
    ctx: mypy.plugin.ClassDefContext,
    auto_attribs_default: bool | None,
    frozen_default: bool,
    slots_default: bool,
) -> bool:
    info = ctx.cls.info

    init = _get_decorator_bool_argument(ctx, "init", True)
    frozen = _get_frozen(ctx, frozen_default)
    order = _determine_eq_order(ctx)
    slots = _get_decorator_bool_argument(ctx, "slots", slots_default)

    auto_attribs = _get_decorator_optional_bool_argument(ctx, "auto_attribs", auto_attribs_default)
    kw_only = _get_decorator_bool_argument(ctx, "kw_only", False)
    match_args = _get_decorator_bool_argument(ctx, "match_args", True)

    for super_info in ctx.cls.info.mro[1:-1]:
        if "attrs_tag" in super_info.metadata and "attrs" not in super_info.metadata:
            # Super class is not ready yet. Request another pass.
            return False

    attributes = _analyze_class(ctx, auto_attribs, kw_only)

    # Check if attribute types are ready.
    for attr in attributes:
        node = info.get(attr.name)
        if node is None:
            # This name is likely blocked by some semantic analysis error that
            # should have been reported already.
            _add_empty_metadata(info)
            return True

    _add_attrs_magic_attribute(ctx, [(attr.name, info[attr.name].type) for attr in attributes])
    if slots:
        _add_slots(ctx, attributes)
    if match_args:
        _add_match_args(ctx, attributes)

    # Save the attributes so that subclasses can reuse them.
    ctx.cls.info.metadata["attrs"] = {
        "attributes": [attr.serialize() for attr in attributes],
        "frozen": frozen,
    }

    adder = MethodAdder(ctx)
    # If  __init__ is not being generated, attrs still generates it as __attrs_init__ instead.
    _add_init(ctx, attributes, adder, "__init__" if init else ATTRS_INIT_NAME)

    if order:
        _add_order(ctx, adder)
    if frozen:
        _make_frozen(ctx, attributes)
        # Frozen classes are hashable by default, even if inheriting from non-frozen ones.
        hashable: bool | None = _get_decorator_bool_argument(
            ctx, "hash", True
        ) and _get_decorator_bool_argument(ctx, "unsafe_hash", True)
    else:
        hashable = _get_decorator_optional_bool_argument(ctx, "unsafe_hash")
        if hashable is None:  # unspecified
            hashable = _get_decorator_optional_bool_argument(ctx, "hash")

    eq = _get_decorator_optional_bool_argument(ctx, "eq")
    has_own_hash = "__hash__" in ctx.cls.info.names

    if has_own_hash or (hashable is None and eq is False):
        pass  # Do nothing.
    elif hashable:
        # We copy the `__hash__` signature from `object` to make them hashable.
        ctx.cls.info.names["__hash__"] = ctx.cls.info.mro[-1].names["__hash__"]
    else:
        _remove_hashability(ctx)

    return True

