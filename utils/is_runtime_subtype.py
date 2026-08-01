
def is_runtime_subtype(left: RType, right: RType) -> bool:
    if isinstance(right, RUnion) and not isinstance(left, RUnion):
        return any(not item.is_unboxed and is_runtime_subtype(left, item) for item in right.items)
    return left.accept(RTSubtypeVisitor(right))

