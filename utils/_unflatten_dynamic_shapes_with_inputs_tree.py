from typing import Any

def _unflatten_dynamic_shapes_with_inputs_tree(
    inputs: list[Any],
    dynamic_shapes: dict[str, Any],
) -> dict[str, Any | None]:
    _, tree_structure = _pytree.tree_flatten(inputs)
    return _pytree.tree_unflatten(dynamic_shapes.values(), tree_structure)

