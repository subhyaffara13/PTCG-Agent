
def detect_diverging_alias(node: TypeAlias, target: Type) -> bool:
    """This detects type aliases that will diverge during type checking.

    For example F = Something[..., F[List[T]]]. At each expansion step this will produce
    *new* type aliases: e.g. F[List[int]], F[List[List[int]]], etc. So we can't detect
    recursion. It is a known problem in the literature, recursive aliases and generic types
    don't always go well together. It looks like there is no known systematic solution yet.

    # TODO: should we handle such aliases using type_recursion counter and some large limit?
    They may be handy in rare cases, e.g. to express a union of non-mixed nested lists:
    Nested = Union[T, Nested[List[T]]] ~> Union[T, List[T], List[List[T]], ...]
    """
    is_recursive = node._is_recursive
    if is_recursive is None:
        is_recursive = node in node.target.accept(CollectAliasesVisitor())
    if not is_recursive:
        # Fast path: this is not a recursive alias at all.
        return False
    # Note we only cache positive case, caching negative case is risky, as this type alias
    # (or more importantly any other alias it uses) may be not ready yet.
    node._is_recursive = True
    visitor = DivergingAliasDetector({node})
    _ = target.accept(visitor)
    return visitor.diverging

