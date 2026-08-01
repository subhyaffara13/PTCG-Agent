
def bbox2distance(points, bbox, max_num_bins, reg_scale, up, eps=0.1):
    """
    Converts bounding box coordinates to distances from a reference point.

    Args:
        points (Tensor): (n, 4) [x, y, w, h], where (x, y) is the center.
        bbox (Tensor): (n, 4) bounding boxes in "xyxy" format.
        max_num_bins (float): Maximum bin value.
        reg_scale (float): Controlling curvarture of W(n).
        up (Tensor): Controlling upper bounds of W(n).
        eps (float): Small value to ensure target < max_num_bins.

    Returns:
        Tensor: Decoded distances.
    """

    reg_scale = abs(reg_scale)
    left = (points[:, 0] - bbox[:, 0]) / (points[..., 2] / reg_scale + 1e-16) - 0.5 * reg_scale
    top = (points[:, 1] - bbox[:, 1]) / (points[..., 3] / reg_scale + 1e-16) - 0.5 * reg_scale
    right = (bbox[:, 2] - points[:, 0]) / (points[..., 2] / reg_scale + 1e-16) - 0.5 * reg_scale
    bottom = (bbox[:, 3] - points[:, 1]) / (points[..., 3] / reg_scale + 1e-16) - 0.5 * reg_scale
    four_lens = torch.stack([left, top, right, bottom], -1)
    four_lens, weight_right, weight_left = translate_gt(four_lens, max_num_bins, reg_scale, up)
    if max_num_bins is not None:
        four_lens = four_lens.clamp(min=0, max=max_num_bins - eps)
    return four_lens.reshape(-1).detach(), weight_right.detach(), weight_left.detach()

