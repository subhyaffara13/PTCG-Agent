from typing import Any

def _get_dim_name_mapping(
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any] | None,
):
    name_to_dim = {}
    for dim in tree_iter(dynamic_shapes, is_leaf=lambda x: isinstance(x, Dim)):
        if dim is None:
            # NOTE: this must denote a non-Tensor or automatic at this point.
            continue
        if isinstance(dim, int):
            continue
        elif isinstance(dim, Dim):
            name_to_dim[dim.__name__] = dim
            if isinstance(dim, _DerivedDim):
                name_to_dim[dim.root.__name__] = dim.root  # type: ignore[attr-defined]
        else:
            if not isinstance(dim, _DimHint):
                raise AssertionError(f"expected dim to be _DimHint, got {type(dim)}")
    return name_to_dim

