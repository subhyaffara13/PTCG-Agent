
def analyze_type_callable_member_access(name: str, typ: FunctionLike, mx: MemberContext) -> Type:
    # Class attribute.
    # TODO super?
    instance_type = typ.items[0].get_instance_type(force_fallback=True)
    if isinstance(instance_type, Instance):
        if not mx.is_operator:
            # When Python sees an operator (eg `3 == 4`), it automatically translates that
            # into something like `int.__eq__(3, 4)` instead of `(3).__eq__(4)` as an
            # optimization.
            #
            # While it normally it doesn't matter which of the two versions are used, it
            # does cause inconsistencies when working with classes. For example, translating
            # `int == int` to `int.__eq__(int)` would not work since `int.__eq__` is meant to
            # compare two int _instances_. What we really want is `type(int).__eq__`, which
            # is meant to compare two types or classes.
            #
            # This check makes sure that when we encounter an operator, we skip looking up
            # the corresponding method in the current instance to avoid this edge case.
            # See https://github.com/python/mypy/pull/1787 for more info.
            # TODO: do not rely on same type variables being present in all constructor overloads.
            result = analyze_class_attribute_access(
                instance_type,
                name,
                mx,
                original_vars=typ.items[0].variables,
                mcs_fallback=typ.fallback,
            )
            if result:
                return result
        # Look up from the 'type' type.
        return _analyze_member_access(name, typ.fallback, mx)
    else:
        assert False, f"Unexpected type {instance_type!r}"

