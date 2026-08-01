
def is_node_in_type_annotation_context(node: nodes.NodeNG) -> bool:
    """Check if node is in type annotation context.

    Check for 'AnnAssign', function 'Arguments',
    or part of function return type annotation.
    """
    current_node, parent_node = node, node.parent
    while True:
        match parent_node:
            case nodes.AnnAssign(annotation=ann) if ann == current_node:
                return True
            case nodes.Arguments() if current_node in (
                *parent_node.annotations,
                *parent_node.posonlyargs_annotations,
                *parent_node.kwonlyargs_annotations,
                parent_node.varargannotation,
                parent_node.kwargannotation,
            ):
                return True
            case nodes.FunctionDef(returns=ret) if ret == current_node:
                return True
        current_node, parent_node = parent_node, parent_node.parent
        if isinstance(parent_node, nodes.Module):
            return False

