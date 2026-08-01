
def affine_grid_generator(theta: Tensor, size: list[int], align_corners: bool):
    torch._check(
        len(size) in (4, 5),
        lambda: "affine_grid_generator needs 4d (spatial) or 5d (volumetric) inputs.",
    )
    if len(size) == 4:
        return _affine_grid_generator_4d(theta, size, align_corners=align_corners)
    else:
        return _affine_grid_generator_5d(theta, size, align_corners=align_corners)

