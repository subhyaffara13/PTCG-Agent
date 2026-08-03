from typing import Any

def _negate_tensors_in_tree(tree: Any) -> Any:
    """Negate all tensors in a pytree structure."""

    def _negate(x: Any) -> Any:
        if isinstance(x, torch.Tensor):
            return -x
        return x

    return pytree.tree_map(_negate, tree)

