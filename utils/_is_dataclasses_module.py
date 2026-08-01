
def _is_dataclasses_module(node: nodes.Module) -> bool:
    """Utility function to check if node is from dataclasses_module."""
    return node.name in DATACLASS_MODULES

