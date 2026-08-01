
def remove_node(model: GraphModule, node: Node, prev_node: Node):
    """Removes the given node from the model by replacing all of its users with
    the given previous node
    """
    # For all of the current node's users, replace the current node with
    # the input quantization observer node
    orig_users = list(node.users.keys())
    for user_node in orig_users:
        user_node.replace_input_with(node, prev_node)

    # Erase the InputEqualizationObserver node
    model.graph.erase_node(node)

