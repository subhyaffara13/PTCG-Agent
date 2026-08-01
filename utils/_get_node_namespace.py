
def _get_node_namespace(node: torch.fx.Node) -> tuple[str, list[str], list[str]]:
    """Get the namespace and scope of the node.

    Example::

        {
            'L__self__': ('', <class 'torchvision.models.resnet.ResNet'>),
            'L__self___avgpool': ('avgpool', <class 'torch.nn.modules.pooling.AdaptiveAvgPool2d'>)
        }

    Will yield

    namespace: ": torchvision.models.resnet.ResNet/avgpool: torch.nn.modules.pooling.AdaptiveAvgPool2d/node_name: node_target"
    class_hierarchy: ["torchvision.models.resnet.ResNet", "torch.nn.modules.pooling.AdaptiveAvgPool2d", <node_target>]
    name_scopes: ["", "avgpool", <node_name>]

    Args:
        node: The node to get the namespace and scope of.

    Returns:
        (namespace, class_hierarchy, name_scope)
    """
    nn_module_stack = node.meta.get("nn_module_stack")
    logger.debug("%s", nn_module_stack)
    if nn_module_stack is None:
        logger.warning(
            "nn_module_stack not found for node '%s'. Skip adding metadata...",
            node.name,
        )
        return f"{node.name}: {node.target}", [str(node.target)], [node.name]
    namespaces = []
    class_hierarchy = []
    name_scopes = []
    for name, nn_module in nn_module_stack.values():
        name_scopes.append(name)
        nn_module_name = _get_qualified_module_name(nn_module)
        class_hierarchy.append(nn_module_name)
        namespaces.append(f"{name}: {_get_qualified_module_name(nn_module)}")
    namespaces.append(f"{node.name}: {node.target}")
    class_hierarchy.append(str(node.target))
    name_scopes.append(node.name)

    return "/".join(namespaces), class_hierarchy, name_scopes

