
def compose_transforms(tf_matrix: Array, other_tf_matrix: Array) -> Array:
    if not broadcastable(tf_matrix.shape, other_tf_matrix.shape):
        len_a = tf_matrix.shape[0] if tf_matrix.ndim == 3 else 1
        len_b = other_tf_matrix.shape[0] if other_tf_matrix.ndim == 3 else 1
        raise ValueError(
            "Expected equal number of transforms in both or a "
            "single transform in either object, got "
            f"{len_a} transforms in first and {len_b}"
            "transforms in second object."
        )
    return tf_matrix @ other_tf_matrix

