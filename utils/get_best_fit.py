
def get_best_fit(
    image_size: tuple[int, int],
    possible_resolutions: torch.Tensor,
    resize_to_max_canvas: bool = False,
) -> tuple[int, int]:
    """
    Determines the best canvas possible from a list of possible resolutions to, without distortion,
    resize an image to.

    For each possible resolution, calculates the scaling factors for
    width and height, and selects the smallest one, which is the limiting side.
    E.g. to match the canvas you can upscale height by 2x, and width by 1.5x,
    therefore, the maximum upscaling you can do is min(2, 1.5) = 1.5.

    If upscaling is possible (any of the scaling factors is greater than 1),
    then picks the smallest upscaling factor > 1, unless resize_to_max_canvas is True.

    If upscaling is not possible, then picks the largest scaling factor <= 1, i.e.
    reduce downscaling as much as possible.

    If there are multiple resolutions with the same max scale, we pick the one with the lowest area,
    to minimize padding. E.g., the same image can be upscaled to 224x224 and 224x448, but the latter
    has more padding.

    Args:
        image_size (tuple[int, int]): A tuple containing the height and width of the image.
        possible_resolutions (torch.Tensor): A tensor of shape (N, 2) where each
            row represents a possible resolution (height, width).
        resize_to_max_canvas (bool): If True, will return the largest upscaling resolution.

    Returns:
        list[int]: The best resolution [height, width] for the given image.

    Example:
        >>> image_size = (200, 300)
        >>> possible_resolutions = torch.tensor([[224, 672],
        ...                                     [672, 224],
        ...                                     [224, 448],
        ...                                     [448, 224],
        ...                                     [224, 224]])
        >>> get_best_fit(image_size, possible_resolutions)
        [224, 448]

        We have:
            scale_w = tensor([2.2400, 0.7467, 1.4933, 0.7467, 0.7467])
            scale_h = tensor([1.1200, 3.3600, 1.1200, 2.2400, 1.1200])
            scales = tensor([1.1200, 0.7467, 1.1200, 0.7467, 0.7467])
        Only one of the scales > 1:
            upscaling_possible = tensor([1.1200, 1.1200])
            smallest_rescale = tensor(1.1200)
        So we pick the resolution with the smallest smallest area:
            areas = tensor([150528, 100352]) # [672, 224], [224, 448]
            optimal_canvas = tensor([224, 448])
    """

    original_height, original_width = image_size

    # get all possible resolutions heights/widths
    target_heights, target_widths = (
        possible_resolutions[:, 0],
        possible_resolutions[:, 1],
    )

    # get scaling factors to resize the image without distortion
    scale_w = target_widths / original_width
    scale_h = target_heights / original_height

    # get the min scale between width and height (limiting side -> no distortion)
    scales = torch.where(scale_h > scale_w, scale_w, scale_h)

    # filter only scales that allow upscaling
    upscaling_options = scales[scales >= 1]
    if len(upscaling_options) > 0:
        if resize_to_max_canvas:
            selected_scale = torch.max(upscaling_options)
        else:
            selected_scale = torch.min(upscaling_options)
    else:
        # no upscaling possible,
        # get the minimum downscaling (max scale for scales<1)
        downscaling_options = scales[scales < 1]
        selected_scale = torch.max(downscaling_options)

    # get all resolutions that support this scaling factor,
    # e.g. you can upscale to 224x224, 224x448, 224x672 without distortion
    chosen_canvas = possible_resolutions[scales == selected_scale]

    # if there are multiple resolutions,
    # get the one with minimum area to reduce padding
    if len(chosen_canvas) > 1:
        areas = chosen_canvas[:, 0] * chosen_canvas[:, 1]
        optimal_idx = torch.argmin(areas)
        optimal_canvas = chosen_canvas[optimal_idx]
    else:
        optimal_canvas = chosen_canvas[0]

    return optimal_canvas

