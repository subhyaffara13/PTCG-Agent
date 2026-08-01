
def _is_a_numpy_module(node: nodes.Name) -> bool:
    """
    Returns True if the node is a representation of a numpy module.

    For example in :
        import numpy as np
        x = np.linspace(1, 2)
    The node <Name.np> is a representation of the numpy module.

    :param node: node to test
    :return: True if the node is a representation of the numpy module.
    """
    module_nickname = node.name
    potential_import_target = [
        x for x in node.lookup(module_nickname)[1] if isinstance(x, nodes.Import)
    ]
    return any(
        ("numpy", module_nickname) in target.names or ("numpy", None) in target.names
        for target in potential_import_target
    )

