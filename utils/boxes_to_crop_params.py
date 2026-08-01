
def boxes_to_crop_params(
    boxes: torch.Tensor,
    output_size: tuple[int, int],
    padding: float = 1.25,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Compute crop center and scale from bounding boxes, applying padding and aspect ratio correction.

    Accepts either a single box `(4,)` or multiple boxes `(num_boxes, 4)` and returns center/scale with a matching
    leading dimension.

    Args:
        boxes (`torch.Tensor` of shape `(4,)` or `(num_boxes, 4)`): Bounding box in
            (center-x, center-y, width, height) format, with values in absolute pixel coordinates.
        output_size (`tuple[int, int]`): Target output size as `(height, width)`, used to compute
            the aspect ratio for scale correction.
        padding (`float`, *optional*, defaults to `1.25`): Multiplicative factor applied to the
            bounding box dimensions, adding context around the region of interest.

    Returns:
        `tuple[torch.Tensor, torch.Tensor]`: A pair `(center, scale)` where `center` has shape
        `(..., 2)` with (x, y) in input-image pixel coordinates, and `scale` has shape `(..., 2)`
        with (width, height) in input-image pixels representing the dimensions of the padded,
        aspect-ratio-corrected crop window.
    """
    center_x, center_y, width, height = boxes.unbind(-1)
    center = torch.stack([center_x, center_y], dim=-1)
    scaled_width = width * padding
    scaled_height = height * padding
    output_height, output_width = output_size
    aspect_ratio = output_width / output_height
    scale = torch.where(
        (scaled_width > scaled_height * aspect_ratio)[..., None],
        torch.stack([scaled_width, scaled_width / aspect_ratio], dim=-1),
        torch.stack([scaled_height * aspect_ratio, scaled_height], dim=-1),
    )
    return center, scale


def boxes_to_crop_params(
    boxes: torch.Tensor,
    output_size: tuple[int, int],
    padding: float = 1.25,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Compute crop center and scale from bounding boxes, applying padding and aspect ratio correction.

    Accepts either a single box `(4,)` or multiple boxes `(num_boxes, 4)` and returns center/scale with a matching
    leading dimension.

    Args:
        boxes (`torch.Tensor` of shape `(4,)` or `(num_boxes, 4)`): Bounding box in
            (center-x, center-y, width, height) format, with values in absolute pixel coordinates.
        output_size (`tuple[int, int]`): Target output size as `(height, width)`, used to compute
            the aspect ratio for scale correction.
        padding (`float`, *optional*, defaults to `1.25`): Multiplicative factor applied to the
            bounding box dimensions, adding context around the region of interest.

    Returns:
        `tuple[torch.Tensor, torch.Tensor]`: A pair `(center, scale)` where `center` has shape
        `(..., 2)` with (x, y) in input-image pixel coordinates, and `scale` has shape `(..., 2)`
        with (width, height) in input-image pixels representing the dimensions of the padded,
        aspect-ratio-corrected crop window.
    """
    center_x, center_y, width, height = boxes.unbind(-1)
    center = torch.stack([center_x, center_y], dim=-1)
    scaled_width = width * padding
    scaled_height = height * padding
    output_height, output_width = output_size
    aspect_ratio = output_width / output_height
    scale = torch.where(
        (scaled_width > scaled_height * aspect_ratio)[..., None],
        torch.stack([scaled_width, scaled_width / aspect_ratio], dim=-1),
        torch.stack([scaled_height * aspect_ratio, scaled_height], dim=-1),
    )
    return center, scale

