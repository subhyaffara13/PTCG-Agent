from typing import Any

def freeze_irnodes(tree: Any) -> Any:
    """Freeze layouts for every IRNode contained in a pytree."""

    if tree is None:
        return None

    def _freeze(node: IRNode) -> IRNode:
        try:
            node.freeze_layout()
        except NotImplementedError:
            pass
        return node

    return tree_map_only(IRNode, _freeze, tree)

