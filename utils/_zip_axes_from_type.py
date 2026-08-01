
def _zip_axes_from_type(
    typ: type[NDFrame], new_axes: Sequence[Index]
) -> dict[str, Index]:
    return {name: new_axes[i] for i, name in enumerate(typ._AXIS_ORDERS)}

