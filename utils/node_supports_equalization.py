
def node_supports_equalization(node: Node, modules) -> bool:
    """Checks if the current node supports equalization
    Currently we only support nn.Linear/F.Linear and nn.Conv/F.conv layers
    """
    if node.op == "call_module":
        return (
            nn_module_supports_equalization(modules[str(node.target)])
            or fused_module_supports_equalization(modules[str(node.target)])
            or custom_module_supports_equalization(modules[str(node.target)])
        )
    elif node.op == "call_function":
        return node.target in [F.linear, F.conv1d, F.conv2d, F.conv3d]
    return False

