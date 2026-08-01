
def is_exception(obj: Any) -> bool:
    return isinstance(obj, BaseException)


def is_exception(node: nodes.ClassDef) -> bool:
    # bw compatibility
    return node.type == "exception"  # type: ignore[no-any-return]

