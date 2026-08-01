
def get_min_tile_covering_grid(
    image_size: tuple[int, int],
    target_patch_size: int,
    max_image_tiles: int,
    covering_threshold: float = 0.9,
) -> tuple[int, int]:
    image_height, image_width = image_size
    image_area = image_width * image_height
    candidate_tile_grids = get_all_supported_aspect_ratios(1, max_image_tiles)
    evaluated_grids = []
    sufficient_covering_grids = []

    for tile_grid in candidate_tile_grids:
        tile_regions = split_image_into_grid(image_height, image_width, tile_grid)
        tile_covering_ratio = (
            sum(compute_patch_covering_area(*region, target_patch_size) for region in tile_regions) / image_area
        )
        evaluated_grids.append((tile_grid, tile_covering_ratio))
        if tile_covering_ratio > covering_threshold:
            sufficient_covering_grids.append((tile_grid, tile_covering_ratio))

    if sufficient_covering_grids:
        return min(sufficient_covering_grids, key=lambda x: (x[0][0] * x[0][1], -x[1]))[0]
    return min(evaluated_grids, key=lambda x: (-x[1], x[0][0] * x[0][1]))[0]


def get_min_tile_covering_grid(
    image_size: tuple[int, int],
    target_patch_size: int,
    max_image_tiles: int,
    covering_threshold: float = 0.9,
) -> tuple[int, int]:
    image_height, image_width = image_size
    image_area = image_width * image_height
    candidate_tile_grids = get_all_supported_aspect_ratios(1, max_image_tiles)
    evaluated_grids = []
    sufficient_covering_grids = []

    for tile_grid in candidate_tile_grids:
        tile_regions = split_image_into_grid(image_height, image_width, tile_grid)
        tile_covering_ratio = (
            sum(compute_patch_covering_area(*region, target_patch_size) for region in tile_regions) / image_area
        )
        evaluated_grids.append((tile_grid, tile_covering_ratio))
        if tile_covering_ratio > covering_threshold:
            sufficient_covering_grids.append((tile_grid, tile_covering_ratio))

    if sufficient_covering_grids:
        return min(sufficient_covering_grids, key=lambda x: (x[0][0] * x[0][1], -x[1]))[0]
    return min(evaluated_grids, key=lambda x: (-x[1], x[0][0] * x[0][1]))[0]

