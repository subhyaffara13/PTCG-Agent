
def false_only(t: Type) -> ProperType:
    """
    Restricted version of t with only False-ish values
    """
    t = get_proper_type(t)

    if not t.can_be_false:
        if state.strict_optional:
            # All values of t are True-ish, so there are no false values in it
            return UninhabitedType(line=t.line)
        else:
            # When strict optional checking is disabled, everything can be
            # False-ish since anything can be None
            return NoneType(line=t.line)
    elif not t.can_be_true:
        # All values of t are already False-ish, so false_only is idempotent in this case
        return t
    elif isinstance(t, UnionType):
        # The false version of a union type is the union of the false versions of its components
        new_items = [false_only(item) for item in t.items]
        can_be_false_items = [item for item in new_items if item.can_be_false]
        return make_simplified_union(can_be_false_items, line=t.line, column=t.column)
    elif isinstance(t, Instance) and t.type.fullname in ("builtins.str", "builtins.bytes"):
        return LiteralType("", fallback=t)
    elif isinstance(t, Instance) and t.type.fullname == "builtins.int":
        return LiteralType(0, fallback=t)
    else:
        ret_type = _get_type_method_ret_type(t, name="__bool__") or _get_type_method_ret_type(
            t, name="__len__"
        )

        if ret_type:
            if not ret_type.can_be_false:
                return UninhabitedType(line=t.line)
        elif isinstance(t, Instance):
            if (t.type.is_final or t.type.is_enum) and state.strict_optional:
                return UninhabitedType(line=t.line)
        elif isinstance(t, LiteralType) and t.is_enum_literal() and state.strict_optional:
            return UninhabitedType(line=t.line)

        new_t = copy_type(t)
        new_t.can_be_true = False
        return new_t

