from typing import Any, Callable

def _generate_key_paths(
    key_path: KeyPath,
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> Iterable[tuple[KeyPath, Any]]:
    if is_leaf and is_leaf(tree):
        yield key_path, tree
        return

    node_type = _get_node_type(tree)
    handler = SUPPORTED_NODES.get(node_type)
    if not handler:
        # This is a leaf
        yield key_path, tree
        return

    flatten_with_keys = handler.flatten_with_keys_fn
    if flatten_with_keys:
        key_children, _ = flatten_with_keys(tree)
        for k, c in key_children:
            yield from _generate_key_paths((*key_path, k), c, is_leaf)
    else:
        # We registered this pytree but didn't add a flatten_with_keys_fn, complain.
        raise ValueError(
            f"Did not find a flatten_with_keys_fn for type: {node_type}. "
            "Please pass a flatten_with_keys_fn argument to register_pytree_node."
        )

