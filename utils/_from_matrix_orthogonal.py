
def _from_matrix_orthogonal(matrix: Array) -> Array:
    """Convert known orthogonal rotation matrix to quaternion"""
    xp = array_namespace(matrix)
    device = xp_device(matrix)

    matrix_trace = matrix[..., 0, 0] + matrix[..., 1, 1] + matrix[..., 2, 2]
    decision = xp.stack(
        [matrix[..., 0, 0], matrix[..., 1, 1], matrix[..., 2, 2], matrix_trace],
        axis=-1,
    )
    choice = xp.argmax(decision, axis=-1, keepdims=True)
    quat = xp.empty((*matrix.shape[:-2], 4), dtype=matrix.dtype, device=device)

    # The Array API does not support mixing integer indexing with ellipsis, so we cannot
    # follow the same pattern as the cython backend. Instead, we compute each case
    # explicitly and assemble the final result with `xp.where`.
    # TODO: Revisit this implementation if the array API supports mixed integer and
    # ellipsis indexing.

    # Case 0
    quat_0 = xp.stack(
        [
            1 - matrix_trace[...] + 2 * matrix[..., 0, 0],
            matrix[..., 1, 0] + matrix[..., 0, 1],
            matrix[..., 2, 0] + matrix[..., 0, 2],
            matrix[..., 2, 1] - matrix[..., 1, 2],
        ],
        axis=-1,
    )
    quat = xp.where(choice == 0, quat_0, quat)

    # Case 1
    quat_1 = xp.stack(
        [
            matrix[..., 1, 0] + matrix[..., 0, 1],
            1 - matrix_trace[...] + 2 * matrix[..., 1, 1],
            matrix[..., 2, 1] + matrix[..., 1, 2],
            matrix[..., 0, 2] - matrix[..., 2, 0],
        ],
        axis=-1,
    )
    quat = xp.where(choice == 1, quat_1, quat)

    # Case 2
    quat_2 = xp.stack(
        [
            matrix[..., 2, 0] + matrix[..., 0, 2],
            matrix[..., 2, 1] + matrix[..., 1, 2],
            1 - matrix_trace[...] + 2 * matrix[..., 2, 2],
            matrix[..., 1, 0] - matrix[..., 0, 1],
        ],
        axis=-1,
    )
    quat = xp.where(choice == 2, quat_2, quat)

    # Case 3
    quat_3 = xp.stack(
        [
            matrix[..., 2, 1] - matrix[..., 1, 2],
            matrix[..., 0, 2] - matrix[..., 2, 0],
            matrix[..., 1, 0] - matrix[..., 0, 1],
            1 + matrix_trace[...],
        ],
        axis=-1,
    )
    quat = xp.where(choice == 3, quat_3, quat)

    return _normalize_quaternion(quat)

