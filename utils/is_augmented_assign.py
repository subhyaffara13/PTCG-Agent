
def is_augmented_assign(node: nodes.Assign) -> tuple[bool, str]:
    """Determine if the node is assigning itself (with modifications) to itself.

    For example: x = 1 + x
    """
    if not isinstance(node.value, nodes.BinOp):
        return False, ""

    binop = node.value
    target = node.targets[0]

    if not isinstance(target, (nodes.AssignName, nodes.AssignAttr, nodes.Subscript)):
        return False, ""

    # We don't want to catch x = "1" + x or x = "%s" % x
    if isinstance(binop.left, nodes.Const) and isinstance(
        binop.left.value, (str, bytes)
    ):
        return False, ""

    # This could probably be improved but for now we disregard all assignments from calls
    if isinstance(binop.left, nodes.Call) or isinstance(binop.right, nodes.Call):
        return False, ""

    if _is_target_name_in_binop_side(target, binop.left):
        return True, binop.op
    if (
        # Unless an operator is commutative, we should not raise (i.e. x = 3/x)
        binop.op in COMMUTATIVE_OPERATORS
        and _is_target_name_in_binop_side(target, binop.right)
    ):
        if isinstance(binop.left, nodes.Const):
            # This bizarrely became necessary after an unrelated call to igetattr().
            # Seems like a code smell uncovered in #10212.
            # tuple(node.frame().igetattr(node.name))
            inferred_left = binop.left
        else:
            inferred_left = safe_infer(binop.left)
        match inferred_left:
            case nodes.Const(value=int()):
                return True, binop.op
        return False, ""
    return False, ""

