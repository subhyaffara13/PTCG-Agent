
def is_magic_method(op: Any) -> bool:
    magic_ops = OrderedSet(method_to_operator(m) for m in magic_methods)
    return op in magic_ops

