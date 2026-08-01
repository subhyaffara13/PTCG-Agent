
def gaussian_blur_preserve_max(heatmaps: torch.Tensor, kernel: int = 11) -> torch.Tensor:
    """Gaussian blur per-keypoint heatmap, preserving the original max value.

    Matches cv2.GaussianBlur with sigma=0 which means that the sigma is automatically
    computed from the kernel size.

    Args:
        heatmaps: Shape `(K, height, width)`.
        kernel: Odd integer kernel size for the Gaussian blur. Must be greater than 1.

    Returns:
        `torch.Tensor`: Blurred heatmaps of the same shape as the input.
    """
    if kernel % 2 == 0 or kernel <= 1:
        raise ValueError("Kernel size must be an odd integer greater than 1.")
    sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8
    border = (kernel - 1) // 2
    origin_maxes = heatmaps.amax(dim=(1, 2))  # (K,)

    # Padding required to prevent border effect from gaussian blur. Torchvision uses reflect padding internally.
    padded = F.pad(heatmaps, (border, border, border, border), mode="constant", value=0.0)
    blurred = tvF.gaussian_blur(padded, kernel_size=[kernel, kernel], sigma=[sigma, sigma])
    result = blurred[:, border:-border, border:-border]

    result_maxes = result.amax(dim=(1, 2))  # (K,)
    safe_maxes = torch.where(result_maxes > 0, result_maxes, torch.ones_like(result_maxes))
    scale = torch.where(result_maxes > 0, origin_maxes / safe_maxes, torch.ones_like(origin_maxes))
    return result * scale[:, None, None]


def gaussian_blur_preserve_max(heatmaps: torch.Tensor, kernel: int = 11) -> torch.Tensor:
    """Gaussian blur per-keypoint heatmap, preserving the original max value.

    Matches cv2.GaussianBlur with sigma=0 which means that the sigma is automatically
    computed from the kernel size.

    Args:
        heatmaps: Shape `(K, height, width)`.
        kernel: Odd integer kernel size for the Gaussian blur. Must be greater than 1.

    Returns:
        `torch.Tensor`: Blurred heatmaps of the same shape as the input.
    """
    if kernel % 2 == 0 or kernel <= 1:
        raise ValueError("Kernel size must be an odd integer greater than 1.")
    sigma = 0.3 * ((kernel - 1) * 0.5 - 1) + 0.8
    border = (kernel - 1) // 2
    origin_maxes = heatmaps.amax(dim=(1, 2))  # (K,)

    # Padding required to prevent border effect from gaussian blur. Torchvision uses reflect padding internally.
    padded = F.pad(heatmaps, (border, border, border, border), mode="constant", value=0.0)
    blurred = tvF.gaussian_blur(padded, kernel_size=[kernel, kernel], sigma=[sigma, sigma])
    result = blurred[:, border:-border, border:-border]

    result_maxes = result.amax(dim=(1, 2))  # (K,)
    safe_maxes = torch.where(result_maxes > 0, result_maxes, torch.ones_like(result_maxes))
    scale = torch.where(result_maxes > 0, origin_maxes / safe_maxes, torch.ones_like(origin_maxes))
    return result * scale[:, None, None]

