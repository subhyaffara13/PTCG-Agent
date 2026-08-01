
def right_inverse(layout: LayoutOrIntTuple | None) -> Layout | None:
    if layout is None:
        return None
    elif is_int(layout):
        return Layout(layout)

    result_shape = []
    result_stride = []
    current_idx = 1

    flat_shape = flatten(layout.shape)  # type: ignore[union-attr]
    flat_stride = flatten(layout.stride)  # type: ignore[union-attr]
    sorted_DSA = sorted(zip(flat_stride, flat_shape, suffix_product(flat_shape)))  # type: ignore[arg-type]
    for stride, shape, rstride in sorted_DSA:
        if shape == 1:
            continue
        if current_idx != stride:
            break

        result_shape.append(shape)
        result_stride.append(rstride)
        current_idx = shape * stride

    result_shape.reverse()
    result_stride.reverse()
    return coalesce(Layout(tuple(result_shape), tuple(result_stride)))

