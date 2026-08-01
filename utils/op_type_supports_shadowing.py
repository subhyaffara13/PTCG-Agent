
def op_type_supports_shadowing(node: Node) -> bool:
    if node.op == "call_function":
        if node.target in (
            torch.add,
            torch.mul,
            operator.add,
            operator.mul,
            torch.cat,
            torch.stack,
        ):
            # shadowing for ops with multiple tensor inputs is not implemented yet
            return False
    return True

