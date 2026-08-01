
def is_gradient_acc(node: Node) -> bool:
    return node.meta.get("is_gradient_acc", False)

