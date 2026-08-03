from typing import Any

def _flatten_dynamic_shapes(
    combined_args: dict[str, Any],
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any],
) -> list[Any]:
    flat_shapes = []

    def _tree_map_helper(path, t, shape):
        nonlocal flat_shapes
        flat_shapes.append(shape)

    _tree_map_with_path(_tree_map_helper, combined_args, dynamic_shapes)
    return flat_shapes

