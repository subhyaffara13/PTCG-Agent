
def _infer_value_type_with_auto_fallback(
    ctx: mypy.plugin.AttributeContext, proper_type: ProperType | None
) -> Type | None:
    """Figure out the type of an enum value accounting for `auto()`.

    This method is a no-op for a `None` proper_type and also in the case where
    the type is not "enum.auto"
    """
    if proper_type is None:
        return None
    proper_type = get_proper_type(fixup_partial_type(proper_type))
    # Enums in stubs may have ... instead of actual values. If `_value_` is annotated
    # (manually or inherited from IntEnum, for example), it is a more reasonable guess
    # than literal ellipsis type.
    if (
        _is_defined_in_stub(ctx)
        and isinstance(proper_type, Instance)
        and proper_type.type.fullname in ELLIPSIS_TYPE_NAMES
        and isinstance(ctx.type, Instance)
    ):
        value_type = ctx.type.type.get("_value_")
        if value_type is not None and isinstance(var := value_type.node, Var):
            return var.type
        return proper_type
    if not (isinstance(proper_type, Instance) and proper_type.type.fullname == "enum.auto"):
        if is_named_instance(proper_type, "enum.member") and proper_type.args:
            return proper_type.args[0]
        return proper_type
    assert isinstance(ctx.type, Instance), "An incorrect ctx.type was passed."
    info = ctx.type.type
    # Find the first _generate_next_value_ on the mro.  We need to know
    # if it is `Enum` because `Enum` types say that the return-value of
    # `_generate_next_value_` is `Any`.  In reality the default `auto()`
    # returns an `int` (presumably the `Any` in typeshed is to make it
    # easier to subclass and change the returned type).
    type_with_gnv = _first(ti for ti in info.mro if ti.names.get("_generate_next_value_"))
    if type_with_gnv is None:
        return ctx.default_attr_type

    stnode = type_with_gnv.names["_generate_next_value_"]

    # This should be a `CallableType`
    node_type = get_proper_type(stnode.type)
    if isinstance(node_type, CallableType):
        if type_with_gnv.fullname == "enum.Enum":
            int_type = ctx.api.named_generic_type("builtins.int", [])
            return int_type
        return get_proper_type(node_type.ret_type)
    return ctx.default_attr_type

