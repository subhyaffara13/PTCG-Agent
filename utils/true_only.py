
def true_only(t: Type) -> ProperType:
    """
    Restricted version of t with only True-ish values
    """
    t = get_proper_type(t)

    if not t.can_be_true:
        # All values of t are False-ish, so there are no true values in it
        return UninhabitedType(line=t.line, column=t.column)
    elif not t.can_be_false:
        # All values of t are already True-ish, so true_only is idempotent in this case
        return t
    elif isinstance(t, UnionType):
        # The true version of a union type is the union of the true versions of its components
        new_items = [true_only(item) for item in t.items]
        can_be_true_items = [item for item in new_items if item.can_be_true]
        return make_simplified_union(can_be_true_items, line=t.line, column=t.column)
    else:
        ret_type = _get_type_method_ret_type(t, name="__bool__") or _get_type_method_ret_type(
            t, name="__len__"
        )

        if ret_type and not ret_type.can_be_true:
            return UninhabitedType(line=t.line, column=t.column)

        new_t = copy_type(t)
        new_t.can_be_false = False
        return new_t

