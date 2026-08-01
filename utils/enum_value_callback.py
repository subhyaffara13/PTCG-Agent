
def enum_value_callback(ctx: mypy.plugin.AttributeContext) -> Type:
    """This plugin refines the 'value' attribute in enums to refer to
    the original underlying value. For example, suppose we have the
    following:

        class SomeEnum:
            FOO = A()
            BAR = B()

    By default, mypy will infer that 'SomeEnum.FOO.value' and
    'SomeEnum.BAR.value' both are of type 'Any'. This plugin refines
    this inference so that mypy understands the expressions are
    actually of types 'A' and 'B' respectively. This better reflects
    the actual runtime behavior.

    This plugin works simply by looking up the original value assigned
    to the enum. For example, when this plugin sees 'SomeEnum.BAR.value',
    it will look up whatever type 'BAR' had in the SomeEnum TypeInfo and
    use that as the inferred type of the overall expression.

    This plugin assumes that the provided context is an attribute access
    matching one of the strings found in 'ENUM_VALUE_ACCESS'.
    """
    enum_field_name = _extract_underlying_field_name(ctx.type)
    if enum_field_name is None:
        # We do not know the enum field name (perhaps it was passed to a
        # function and we only know that it _is_ a member).  All is not lost
        # however, if we can prove that the all of the enum members have the
        # same value-type, then it doesn't matter which member was passed in.
        # The value-type is still known.
        if isinstance(ctx.type, Instance):
            info = ctx.type.type

            # As long as mypy doesn't understand attribute creation in __new__,
            # there is no way to predict the value type if the enum class has a
            # custom implementation
            if _implements_new(info):
                return ctx.default_attr_type

            stnodes = (info.get(name) for name in info.names)

            # Enums _can_ have methods, instance attributes, and `nonmember`s.
            # Omit methods and attributes created by assigning to self.*
            # for our value inference.
            node_types = (
                get_proper_type(n.type) if n else None
                for n in stnodes
                if n is None or not n.implicit
            )
            proper_types = [
                _infer_value_type_with_auto_fallback(ctx, t)
                for t in node_types
                if t is None
                or (not isinstance(t, CallableType) and not is_named_instance(t, "enum.nonmember"))
            ]
            underlying_type = _first(proper_types)
            if underlying_type is None:
                return ctx.default_attr_type

            # At first we try to predict future `value` type if all other items
            # have the same type. For example, `int`.
            # If this is the case, we simply return this type.
            # See https://github.com/python/mypy/pull/9443
            all_same_value_type = all(
                proper_type is not None and proper_type == underlying_type
                for proper_type in proper_types
            )
            if all_same_value_type:
                if underlying_type is not None:
                    return underlying_type

            # But, after we started treating all `Enum` values as `Final`,
            # we start to infer types in
            # `item = 1` as `Literal[1]`, not just `int`.
            # So, for example types in this `Enum` will all be different:
            #
            #  class Ordering(IntEnum):
            #      one = 1
            #      two = 2
            #      three = 3
            #
            # We will infer three `Literal` types here.
            # They are not the same, but they are equivalent.
            # So, we unify them to make sure `.value` prediction still works.
            # Result will be `Literal[1] | Literal[2] | Literal[3]` for this case.
            all_equivalent_types = all(
                proper_type is not None and is_equivalent(proper_type, underlying_type)
                for proper_type in proper_types
            )
            if all_equivalent_types:
                return make_simplified_union(cast(Sequence[Type], proper_types))
        return ctx.default_attr_type

    assert isinstance(ctx.type, Instance)
    info = ctx.type.type

    # As long as mypy doesn't understand attribute creation in __new__,
    # there is no way to predict the value type if the enum class has a
    # custom implementation
    if _implements_new(info):
        return ctx.default_attr_type

    stnode = info.get(enum_field_name)
    if stnode is None:
        return ctx.default_attr_type

    underlying_type = _infer_value_type_with_auto_fallback(ctx, get_proper_type(stnode.type))
    if underlying_type is None:
        return ctx.default_attr_type

    return underlying_type

