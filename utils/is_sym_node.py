
def is_sym_node(node: _HasMeta) -> bool:
    if not hasattr(node, "meta"):
        raise AssertionError("All nodes traced with proxy_tensor should have meta")
    return "val" in node.meta and isinstance(node.meta["val"], py_sym_types)

