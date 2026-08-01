
def distance2bbox(points, distance: torch.Tensor, reg_scale: float) -> torch.Tensor:
    """
    Decodes edge-distances into bounding box coordinates.

    Args:
        points (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
        distance (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4), representing distances from the point to the left, top, right, and bottom boundaries.
        reg_scale (`float`):
            Controls the curvature of the Weighting Function.
    Returns:
        `torch.Tensor`: Bounding boxes in (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
    """
    reg_scale = abs(reg_scale)
    top_left_x = points[..., 0] - (0.5 * reg_scale + distance[..., 0]) * (points[..., 2] / reg_scale)
    top_left_y = points[..., 1] - (0.5 * reg_scale + distance[..., 1]) * (points[..., 3] / reg_scale)
    bottom_right_x = points[..., 0] + (0.5 * reg_scale + distance[..., 2]) * (points[..., 2] / reg_scale)
    bottom_right_y = points[..., 1] + (0.5 * reg_scale + distance[..., 3]) * (points[..., 3] / reg_scale)

    bboxes = torch.stack([top_left_x, top_left_y, bottom_right_x, bottom_right_y], -1)

    return corners_to_center_format(bboxes)


def distance2bbox(points, distance: torch.Tensor, reg_scale: float) -> torch.Tensor:
    """
    Decodes edge-distances into bounding box coordinates.

    Args:
        points (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
        distance (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4), representing distances from the point to the left, top, right, and bottom boundaries.
        reg_scale (`float`):
            Controls the curvature of the Weighting Function.
    Returns:
        `torch.Tensor`: Bounding boxes in (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
    """
    reg_scale = abs(reg_scale)
    top_left_x = points[..., 0] - (0.5 * reg_scale + distance[..., 0]) * (points[..., 2] / reg_scale)
    top_left_y = points[..., 1] - (0.5 * reg_scale + distance[..., 1]) * (points[..., 3] / reg_scale)
    bottom_right_x = points[..., 0] + (0.5 * reg_scale + distance[..., 2]) * (points[..., 2] / reg_scale)
    bottom_right_y = points[..., 1] + (0.5 * reg_scale + distance[..., 3]) * (points[..., 3] / reg_scale)

    bboxes = torch.stack([top_left_x, top_left_y, bottom_right_x, bottom_right_y], -1)

    return corners_to_center_format(bboxes)


def distance2bbox(points, distance: torch.Tensor, reg_scale: float) -> torch.Tensor:
    """
    Decodes edge-distances into bounding box coordinates.

    Args:
        points (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
        distance (`torch.Tensor`):
            (batch_size, num_boxes, 4) or (num_boxes, 4), representing distances from the point to the left, top, right, and bottom boundaries.
        reg_scale (`float`):
            Controls the curvature of the Weighting Function.
    Returns:
        `torch.Tensor`: Bounding boxes in (batch_size, num_boxes, 4) or (num_boxes, 4) format, representing [x_center, y_center, width, height]
    """
    reg_scale = abs(reg_scale)
    top_left_x = points[..., 0] - (0.5 * reg_scale + distance[..., 0]) * (points[..., 2] / reg_scale)
    top_left_y = points[..., 1] - (0.5 * reg_scale + distance[..., 1]) * (points[..., 3] / reg_scale)
    bottom_right_x = points[..., 0] + (0.5 * reg_scale + distance[..., 2]) * (points[..., 2] / reg_scale)
    bottom_right_y = points[..., 1] + (0.5 * reg_scale + distance[..., 3]) * (points[..., 3] / reg_scale)

    bboxes = torch.stack([top_left_x, top_left_y, bottom_right_x, bottom_right_y], -1)

    return corners_to_center_format(bboxes)

