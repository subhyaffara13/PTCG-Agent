from typing import Any

def _flatten_dynamic_shapes_to_axes(
    dynamic_shapes: dict[str, Any | None] | tuple[Any, ...] | list[Any],
) -> tuple[list[Any], _pytree.TreeSpec]:
    # If it's a dict/list/tuple with torch.export.Dim, we consider it's an axis to dim mapping
    def is_axes(x) -> bool:
        return (
            isinstance(x, dict)
            and all(
                isinstance(k, int)
                and (v is None or isinstance(v, (Dim, _DimHint, str, int)))
                for k, v in x.items()
            )
        ) or (
            isinstance(x, (list, tuple))
            and all(v is None or isinstance(v, (Dim, _DimHint, str, int)) for v in x)
        )

    return _pytree.tree_flatten(dynamic_shapes, is_leaf=is_axes)

