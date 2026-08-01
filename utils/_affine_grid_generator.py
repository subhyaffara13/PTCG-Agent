
def _affine_grid_generator(
    g: jit_utils.GraphContext,
    theta: _C.Value,
    size: _C.Value,
    align_corners: bool,
):
    return g.op(
        "AffineGrid",
        theta,
        size,
        align_corners_i=int(align_corners),
    )

