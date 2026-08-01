
def compute_reduction_output_shape(
    shape: ShapeType, dimensions: Sequence
) -> tuple[int, ...]:
    for idx in dimensions:
        validate_idx(len(shape), idx)

    new_shape = []
    for idx in range(len(shape)):
        if idx in dimensions:
            continue

        new_shape.append(shape[idx])

    return tuple(new_shape)

