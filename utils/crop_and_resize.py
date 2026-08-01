
def crop_and_resize(
    image: torch.Tensor,
    boxes: torch.Tensor,
    output_size: tuple[int, int],
    padding: float = 1.25,
) -> torch.Tensor:
    """Crops and resizes bounding box regions from the input image to the target output size.

    Applies padding and aspect ratio correction to each crop before resizing.
    Uses bilinear interpolation for downscaling and bicubic for upscaling.

    This implementation is equivalent to the cv2 affine warp with rotation=0 used in the original
    Sapiens2 codebase. Rotation is always zero because we don't support rotated bounding boxes.

    Args:
        image (`torch.Tensor`): Input image tensor of shape `(C, H, W)` in float32.
        boxes (`torch.Tensor`): Bounding boxes in (center-x, center-y, width, height) format,
            shape `(num_boxes, 4)`, with values in absolute pixel coordinates.
        output_size (`tuple[int, int]`): Target output size as `(height, width)`.
        padding (`float`, *optional*, defaults to `1.25`): Multiplicative factor applied to the
            bounding box dimensions before cropping, adding context around the region of interest.

    Returns:
        `torch.Tensor`: Cropped and resized images of shape `(num_boxes, C, output_height, output_width)`.
    """
    output_height, output_width = output_size
    num_channels, input_height, input_width = image.shape
    center, scale = boxes_to_crop_params(boxes, output_size=output_size, padding=padding)
    center_x, center_y = center.unbind(-1)
    boxes_width, boxes_height = scale.unbind(-1)

    scale_x = (output_width - 1) / boxes_width  # (num_boxes,)
    scale_y = (output_height - 1) / boxes_height  # (num_boxes,)
    is_bilinear = torch.minimum(scale_x, scale_y) < 1.0  # (num_boxes,)

    grid_y, grid_x = torch.meshgrid(
        torch.arange(output_height, dtype=torch.float32, device=image.device),
        torch.arange(output_width, dtype=torch.float32, device=image.device),
        indexing="ij",
    )
    in_x = grid_x / scale_x[:, None, None] + center_x[:, None, None] - 0.5 * boxes_width[:, None, None]
    in_y = grid_y / scale_y[:, None, None] + center_y[:, None, None] - 0.5 * boxes_height[:, None, None]
    # (num_boxes, output_height, output_width, 2)
    grids = torch.stack([2.0 * in_x / (input_width - 1) - 1.0, 2.0 * in_y / (input_height - 1) - 1.0], dim=-1)

    num_boxes = boxes.shape[0]
    output = torch.empty(num_boxes, num_channels, output_height, output_width, device=image.device, dtype=image.dtype)

    # Apply grid sampling separately for upscaling and downscaling to use the appropriate interpolation mode
    image_4d = image.unsqueeze(0)
    for mask, mode in [(is_bilinear, "bilinear"), (~is_bilinear, "bicubic")]:
        if mask.any():
            output[mask] = F.grid_sample(
                image_4d.expand(mask.sum(), -1, -1, -1),
                grids[mask],
                mode=mode,
                padding_mode="zeros",
                align_corners=True,
            )

    return output


def crop_and_resize(
    image: torch.Tensor,
    boxes: torch.Tensor,
    output_size: tuple[int, int],
    padding: float = 1.25,
) -> torch.Tensor:
    """Crops and resizes bounding box regions from the input image to the target output size.

    Applies padding and aspect ratio correction to each crop before resizing.
    Uses bilinear interpolation for downscaling and bicubic for upscaling.

    This implementation is equivalent to the cv2 affine warp with rotation=0 used in the original
    Sapiens2 codebase. Rotation is always zero because we don't support rotated bounding boxes.

    Args:
        image (`torch.Tensor`): Input image tensor of shape `(C, H, W)` in float32.
        boxes (`torch.Tensor`): Bounding boxes in (center-x, center-y, width, height) format,
            shape `(num_boxes, 4)`, with values in absolute pixel coordinates.
        output_size (`tuple[int, int]`): Target output size as `(height, width)`.
        padding (`float`, *optional*, defaults to `1.25`): Multiplicative factor applied to the
            bounding box dimensions before cropping, adding context around the region of interest.

    Returns:
        `torch.Tensor`: Cropped and resized images of shape `(num_boxes, C, output_height, output_width)`.
    """
    output_height, output_width = output_size
    num_channels, input_height, input_width = image.shape
    center, scale = boxes_to_crop_params(boxes, output_size=output_size, padding=padding)
    center_x, center_y = center.unbind(-1)
    boxes_width, boxes_height = scale.unbind(-1)

    scale_x = (output_width - 1) / boxes_width  # (num_boxes,)
    scale_y = (output_height - 1) / boxes_height  # (num_boxes,)
    is_bilinear = torch.minimum(scale_x, scale_y) < 1.0  # (num_boxes,)

    grid_y, grid_x = torch.meshgrid(
        torch.arange(output_height, dtype=torch.float32, device=image.device),
        torch.arange(output_width, dtype=torch.float32, device=image.device),
        indexing="ij",
    )
    in_x = grid_x / scale_x[:, None, None] + center_x[:, None, None] - 0.5 * boxes_width[:, None, None]
    in_y = grid_y / scale_y[:, None, None] + center_y[:, None, None] - 0.5 * boxes_height[:, None, None]
    # (num_boxes, output_height, output_width, 2)
    grids = torch.stack([2.0 * in_x / (input_width - 1) - 1.0, 2.0 * in_y / (input_height - 1) - 1.0], dim=-1)

    num_boxes = boxes.shape[0]
    output = torch.empty(num_boxes, num_channels, output_height, output_width, device=image.device, dtype=image.dtype)

    # Apply grid sampling separately for upscaling and downscaling to use the appropriate interpolation mode
    image_4d = image.unsqueeze(0)
    for mask, mode in [(is_bilinear, "bilinear"), (~is_bilinear, "bicubic")]:
        if mask.any():
            output[mask] = F.grid_sample(
                image_4d.expand(mask.sum(), -1, -1, -1),
                grids[mask],
                mode=mode,
                padding_mode="zeros",
                align_corners=True,
            )

    return output

