
def handle_recursive_union(template: UnionType, actual: Type, direction: int) -> list[Constraint]:
    # This is a hack to special-case things like Union[T, Inst[T]] in recursive types. Although
    # it is quite arbitrary, it is a relatively common pattern, so we should handle it well.
    # This function may be called when inferring against such union resulted in different
    # constraints for each item. Normally we give up in such case, but here we instead split
    # the union in two parts, and try inferring sequentially.
    non_type_var_items = [t for t in template.items if not isinstance(t, TypeVarType)]
    type_var_items = [t for t in template.items if isinstance(t, TypeVarType)]
    return infer_constraints(
        UnionType.make_union(non_type_var_items), actual, direction
    ) or infer_constraints(UnionType.make_union(type_var_items), actual, direction)

