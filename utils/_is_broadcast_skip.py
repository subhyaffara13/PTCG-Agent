
def _is_broadcast_skip(input_shape, skip_shape):
    """Check if skip_shape can broadcast to input_shape for SkipLayerNormalization.

    The kernel supports: input 3D (B,S,H) with skip 3D (1,S,H) or skip 2D (S,H).
    """
    if len(input_shape) != 3:
        return False
    if len(skip_shape) == 3:
        return skip_shape[0] == 1 and skip_shape[1] == input_shape[1] and skip_shape[2] == input_shape[2]
    if len(skip_shape) == 2:
        return skip_shape[0] == input_shape[1] and skip_shape[1] == input_shape[2]
    return False

