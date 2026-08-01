
def enumerate_filter_symints(lst: Iterable[IntLikeType]) -> list[tuple[int, SymInt]]:
    # Capture all SymInts from the iterable.
    def symint_check(s: IntLikeType) -> TypeGuard[SymInt]:
        return isinstance(s, SymInt) and not s.node.is_nested_int()

    return [(i, s) for i, s in enumerate(lst) if symint_check(s)]

