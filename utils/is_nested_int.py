
def is_nested_int(s: IntLikeType | FloatLikeType) -> TypeGuard[SymInt]:
    return isinstance(s, torch.SymInt) and s.node.is_nested_int()

