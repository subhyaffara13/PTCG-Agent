
def _generate_crop_boxes(
    image,
    target_size: int,
    crop_n_layers: int = 0,
    overlap_ratio: float = 512 / 1500,
    points_per_crop: int | None = 32,
    crop_n_points_downscale_factor: list[int] | None = 1,
) -> tuple[list[list[int]], list[int]]:
    """
    Generates a list of crop boxes of different sizes. Each layer has (2**i)**2 boxes for the ith layer.

    Args:
        image (`np.ndarray`):
            Image to generate crops for.
        target_size (`int`):
            Size of the smallest crop.
        crop_n_layers (`int`, *optional*):
            If `crops_n_layers>0`, mask prediction will be run again on crops of the image. Sets the number of layers
            to run, where each layer has 2**i_layer number of image crops.
        overlap_ratio (`int`, *optional*):
            Sets the degree to which crops overlap. In the first crop layer, crops will overlap by this fraction of the
            image length. Later layers with more crops scale down this overlap.
        points_per_crop (`int`, *optional*):
            Number of points to sample per crop.
        crop_n_points_downscale_factor (`int`, *optional*):
            The number of points-per-side sampled in layer n is scaled down by crop_n_points_downscale_factor**n.
    """

    if isinstance(image, list):
        raise ValueError("Only one image is allowed for crop generation.")
    original_size = image.shape[-2:]

    points_grid = []
    for i in range(crop_n_layers + 1):
        n_points = int(points_per_crop / (crop_n_points_downscale_factor**i))
        points_grid.append(_build_point_grid(n_points))

    crop_boxes, layer_idxs = _generate_per_layer_crops(crop_n_layers, overlap_ratio, original_size)

    cropped_images, point_grid_per_crop = _generate_crop_images(
        crop_boxes, image, points_grid, layer_idxs, target_size, original_size
    )
    crop_boxes = np.array(crop_boxes)
    crop_boxes = crop_boxes.astype(np.float32)
    points_per_crop = np.array([point_grid_per_crop])
    points_per_crop = np.transpose(points_per_crop, axes=(0, 2, 1, 3))

    input_labels = np.ones_like(points_per_crop[:, :, :, 0], dtype=np.int64)

    return crop_boxes, points_per_crop, cropped_images, input_labels


def _generate_crop_boxes(
    image,
    target_size: int,
    crop_n_layers: int = 0,
    overlap_ratio: float = 512 / 1500,
    points_per_crop: int | None = 32,
    crop_n_points_downscale_factor: list[int] | None = 1,
) -> tuple[list[list[int]], list[int]]:
    """
    Generates a list of crop boxes of different sizes. Each layer has (2**i)**2 boxes for the ith layer.

    Args:
        image (`torch.Tensor`):
            Image to generate crops for.
        target_size (`int`):
            Size of the smallest crop.
        crop_n_layers (`int`, *optional*):
            If `crops_n_layers>0`, mask prediction will be run again on crops of the image. Sets the number of layers
            to run, where each layer has 2**i_layer number of image crops.
        overlap_ratio (`int`, *optional*):
            Sets the degree to which crops overlap. In the first crop layer, crops will overlap by this fraction of the
            image length. Later layers with more crops scale down this overlap.
        points_per_crop (`int`, *optional*):
            Number of points to sample per crop.
        crop_n_points_downscale_factor (`int`, *optional*):
            The number of points-per-side sampled in layer n is scaled down by crop_n_points_downscale_factor**n.
    """

    if isinstance(image, list):
        raise ValueError("Only one image is allowed for crop generation.")
    original_size = image.shape[-2:]

    points_grid = []
    for i in range(crop_n_layers + 1):
        n_points = int(points_per_crop / (crop_n_points_downscale_factor**i))
        points_grid.append(_build_point_grid(n_points))

    crop_boxes, layer_idxs = _generate_per_layer_crops(crop_n_layers, overlap_ratio, original_size)

    cropped_images, point_grid_per_crop = _generate_crop_images(
        crop_boxes, image, points_grid, layer_idxs, target_size, original_size
    )
    crop_boxes = torch.tensor(crop_boxes)
    crop_boxes = crop_boxes.float()
    points_per_crop = torch.stack(point_grid_per_crop)
    points_per_crop = points_per_crop.unsqueeze(0).permute(0, 2, 1, 3)
    cropped_images = torch.stack(cropped_images)

    input_labels = torch.ones_like(points_per_crop[:, :, :, 0], dtype=torch.int64)

    return crop_boxes, points_per_crop, cropped_images, input_labels


def _generate_crop_boxes(
    image,
    target_size: int,
    crop_n_layers: int = 0,
    overlap_ratio: float = 512 / 1500,
    points_per_crop: int | None = 32,
    crop_n_points_downscale_factor: list[int] | None = 1,
) -> tuple[list[list[int]], list[int]]:
    """
    Generates a list of crop boxes of different sizes. Each layer has (2**i)**2 boxes for the ith layer.

    Args:
        image (`torch.Tensor`):
            Image to generate crops for.
        target_size (`int`):
            Size of the smallest crop.
        crop_n_layers (`int`, *optional*):
            If `crops_n_layers>0`, mask prediction will be run again on crops of the image. Sets the number of layers
            to run, where each layer has 2**i_layer number of image crops.
        overlap_ratio (`int`, *optional*):
            Sets the degree to which crops overlap. In the first crop layer, crops will overlap by this fraction of the
            image length. Later layers with more crops scale down this overlap.
        points_per_crop (`int`, *optional*):
            Number of points to sam2ple per crop.
        crop_n_points_downscale_factor (`int`, *optional*):
            The number of points-per-side sam2pled in layer n is scaled down by crop_n_points_downscale_factor**n.
    """

    if isinstance(image, list):
        raise ValueError("Only one image is allowed for crop generation.")
    original_size = image.shape[-2:]

    points_grid = []
    for i in range(crop_n_layers + 1):
        n_points = int(points_per_crop / (crop_n_points_downscale_factor**i))
        points_grid.append(_build_point_grid(n_points))

    crop_boxes, layer_idxs = _generate_per_layer_crops(crop_n_layers, overlap_ratio, original_size)

    cropped_images, point_grid_per_crop = _generate_crop_images(
        crop_boxes, image, points_grid, layer_idxs, target_size, original_size
    )
    crop_boxes = torch.tensor(crop_boxes)
    crop_boxes = crop_boxes.float()
    points_per_crop = torch.stack(point_grid_per_crop)
    points_per_crop = points_per_crop.unsqueeze(0).permute(0, 2, 1, 3)
    cropped_images = torch.stack(cropped_images)

    input_labels = torch.ones_like(points_per_crop[:, :, :, 0], dtype=torch.int64)

    return crop_boxes, points_per_crop, cropped_images, input_labels


def _generate_crop_boxes(
    image,
    target_size: int,
    crop_n_layers: int = 0,
    overlap_ratio: float = 512 / 1500,
    points_per_crop: int | None = 32,
    crop_n_points_downscale_factor: list[int] | None = 1,
) -> tuple[list[list[int]], list[int]]:
    """
    Generates a list of crop boxes of different sizes. Each layer has (2**i)**2 boxes for the ith layer.

    Args:
        image (`torch.Tensor`):
            Image to generate crops for.
        target_size (`int`):
            Size of the smallest crop.
        crop_n_layers (`int`, *optional*):
            If `crops_n_layers>0`, mask prediction will be run again on crops of the image. Sets the number of layers
            to run, where each layer has 2**i_layer number of image crops.
        overlap_ratio (`int`, *optional*):
            Sets the degree to which crops overlap. In the first crop layer, crops will overlap by this fraction of the
            image length. Later layers with more crops scale down this overlap.
        points_per_crop (`int`, *optional*):
            Number of points to sam3ple per crop.
        crop_n_points_downscale_factor (`int`, *optional*):
            The number of points-per-side sam3pled in layer n is scaled down by crop_n_points_downscale_factor**n.
    """

    if isinstance(image, list):
        raise ValueError("Only one image is allowed for crop generation.")
    original_size = image.shape[-2:]

    points_grid = []
    for i in range(crop_n_layers + 1):
        n_points = int(points_per_crop / (crop_n_points_downscale_factor**i))
        points_grid.append(_build_point_grid(n_points))

    crop_boxes, layer_idxs = _generate_per_layer_crops(crop_n_layers, overlap_ratio, original_size)

    cropped_images, point_grid_per_crop = _generate_crop_images(
        crop_boxes, image, points_grid, layer_idxs, target_size, original_size
    )
    crop_boxes = torch.tensor(crop_boxes)
    crop_boxes = crop_boxes.float()
    points_per_crop = torch.stack(point_grid_per_crop)
    points_per_crop = points_per_crop.unsqueeze(0).permute(0, 2, 1, 3)
    cropped_images = torch.stack(cropped_images)

    input_labels = torch.ones_like(points_per_crop[:, :, :, 0], dtype=torch.int64)

    return crop_boxes, points_per_crop, cropped_images, input_labels

