
def post_dark_unbiased_data_processing(
    keypoints: torch.Tensor, heatmaps: torch.Tensor, blur_kernel_size: int = 11
) -> torch.Tensor:
    """Sub-pixel refinement via Hessian on log-heatmaps (UDP Dark Pose).

    Args:
        keypoints: Shape `(num_persons, num_keypoints, 2)` x/y in heatmap pixel coordinates.
        heatmaps: Shape `(num_persons, num_keypoints, height, width)`.

    Returns:
        `(num_persons, num_keypoints, 2)` refined keypoint locations.
    """
    num_persons, num_keypoints, heatmap_height, heatmap_width = heatmaps.shape
    device = heatmaps.device

    heatmaps = gaussian_blur_preserve_max(
        heatmaps.reshape(num_persons * num_keypoints, heatmap_height, heatmap_width), blur_kernel_size
    ).reshape(num_persons, num_keypoints, heatmap_height, heatmap_width)
    heatmaps = heatmaps.clamp(1e-3, 50.0).log()  # Clamp values based on original Sapiens2 implementation

    heatmaps_padded = F.pad(heatmaps, (1, 1, 1, 1), mode="replicate")
    heatmaps_flattened = heatmaps_padded.flatten()

    padded_height = heatmap_height + 2
    padded_width = heatmap_width + 2
    keypoint_stride = padded_height * padded_width
    person_stride = num_keypoints * keypoint_stride

    index = keypoints[:, :, 0].long() + 1 + (keypoints[:, :, 1].long() + 1) * padded_width
    index = index + keypoint_stride * torch.arange(num_keypoints, device=device, dtype=torch.long)[None, :]
    index = index + person_stride * torch.arange(num_persons, device=device, dtype=torch.long)[:, None]
    index = index.unsqueeze(-1)  # (num_persons, num_keypoints, 1)

    position_to_index_offset = {
        (0, 0): 0,
        (0, 1): 1,
        (0, -1): -1,
        (1, 0): padded_width,
        (-1, 0): -padded_width,
        (1, 1): padded_width + 1,
        (-1, -1): -(padded_width + 1),
    }
    # Dict mapping from (dx, dy) offsets to the corresponding values in the heatmap
    heatmap_values = {
        (dx, dy): heatmaps_flattened[index + offset] for (dx, dy), offset in position_to_index_offset.items()
    }

    gradient_x = 0.5 * (heatmap_values[0, 1] - heatmap_values[0, -1])
    gradient_y = 0.5 * (heatmap_values[1, 0] - heatmap_values[-1, 0])

    hessian_xx = heatmap_values[0, 1] - 2 * heatmap_values[0, 0] + heatmap_values[0, -1]
    hessian_yy = heatmap_values[1, 0] - 2 * heatmap_values[0, 0] + heatmap_values[-1, 0]
    hessian_xy = 0.5 * (
        heatmap_values[1, 1]
        - heatmap_values[0, 1]
        - heatmap_values[1, 0]
        + heatmap_values[0, 0]
        + heatmap_values[0, 0]
        - heatmap_values[0, -1]
        - heatmap_values[-1, 0]
        + heatmap_values[-1, -1]
    )

    eps = torch.finfo(hessian_xx.dtype).eps
    hessian_xx = hessian_xx + eps
    hessian_yy = hessian_yy + eps
    determinant = hessian_xx * hessian_yy - hessian_xy * hessian_xy
    offset_x = (hessian_yy * gradient_x - hessian_xy * gradient_y) / determinant
    offset_y = (-hessian_xy * gradient_x + hessian_xx * gradient_y) / determinant
    return keypoints - torch.cat([offset_x, offset_y], dim=-1)


def post_dark_unbiased_data_processing(
    keypoints: torch.Tensor, heatmaps: torch.Tensor, blur_kernel_size: int = 11
) -> torch.Tensor:
    """Sub-pixel refinement via Hessian on log-heatmaps (UDP Dark Pose).

    Args:
        keypoints: Shape `(num_persons, num_keypoints, 2)` x/y in heatmap pixel coordinates.
        heatmaps: Shape `(num_persons, num_keypoints, height, width)`.

    Returns:
        `(num_persons, num_keypoints, 2)` refined keypoint locations.
    """
    num_persons, num_keypoints, heatmap_height, heatmap_width = heatmaps.shape
    device = heatmaps.device

    heatmaps = gaussian_blur_preserve_max(
        heatmaps.reshape(num_persons * num_keypoints, heatmap_height, heatmap_width), blur_kernel_size
    ).reshape(num_persons, num_keypoints, heatmap_height, heatmap_width)
    heatmaps = heatmaps.clamp(1e-3, 50.0).log()  # Clamp values based on original Sapiens2 implementation

    heatmaps_padded = F.pad(heatmaps, (1, 1, 1, 1), mode="replicate")
    heatmaps_flattened = heatmaps_padded.flatten()

    padded_height = heatmap_height + 2
    padded_width = heatmap_width + 2
    keypoint_stride = padded_height * padded_width
    person_stride = num_keypoints * keypoint_stride

    index = keypoints[:, :, 0].long() + 1 + (keypoints[:, :, 1].long() + 1) * padded_width
    index = index + keypoint_stride * torch.arange(num_keypoints, device=device, dtype=torch.long)[None, :]
    index = index + person_stride * torch.arange(num_persons, device=device, dtype=torch.long)[:, None]
    index = index.unsqueeze(-1)  # (num_persons, num_keypoints, 1)

    position_to_index_offset = {
        (0, 0): 0,
        (0, 1): 1,
        (0, -1): -1,
        (1, 0): padded_width,
        (-1, 0): -padded_width,
        (1, 1): padded_width + 1,
        (-1, -1): -(padded_width + 1),
    }
    # Dict mapping from (dx, dy) offsets to the corresponding values in the heatmap
    heatmap_values = {
        (dx, dy): heatmaps_flattened[index + offset] for (dx, dy), offset in position_to_index_offset.items()
    }

    gradient_x = 0.5 * (heatmap_values[0, 1] - heatmap_values[0, -1])
    gradient_y = 0.5 * (heatmap_values[1, 0] - heatmap_values[-1, 0])

    hessian_xx = heatmap_values[0, 1] - 2 * heatmap_values[0, 0] + heatmap_values[0, -1]
    hessian_yy = heatmap_values[1, 0] - 2 * heatmap_values[0, 0] + heatmap_values[-1, 0]
    hessian_xy = 0.5 * (
        heatmap_values[1, 1]
        - heatmap_values[0, 1]
        - heatmap_values[1, 0]
        + heatmap_values[0, 0]
        + heatmap_values[0, 0]
        - heatmap_values[0, -1]
        - heatmap_values[-1, 0]
        + heatmap_values[-1, -1]
    )

    eps = torch.finfo(hessian_xx.dtype).eps
    hessian_xx = hessian_xx + eps
    hessian_yy = hessian_yy + eps
    determinant = hessian_xx * hessian_yy - hessian_xy * hessian_xy
    offset_x = (hessian_yy * gradient_x - hessian_xy * gradient_y) / determinant
    offset_y = (-hessian_xy * gradient_x + hessian_xx * gradient_y) / determinant
    return keypoints - torch.cat([offset_x, offset_y], dim=-1)


def post_dark_unbiased_data_processing(coords: np.ndarray, batch_heatmaps: np.ndarray, kernel: int = 3) -> np.ndarray:
    """DARK post-pocessing. Implemented by unbiased_data_processing.

    Paper references:
    - Huang et al. The Devil is in the Details: Delving into Unbiased Data Processing for Human Pose Estimation (CVPR 2020).
    - Zhang et al. Distribution-Aware Coordinate Representation for Human Pose Estimation (CVPR 2020).

    Args:
        coords (`np.ndarray` of shape `(num_persons, num_keypoints, 2)`):
            Initial coordinates of human pose.
        batch_heatmaps (`np.ndarray` of shape `(batch_size, num_keypoints, height, width)`):
            Batched heatmaps as predicted by the model.
            A batch_size of 1 is used for the bottom up paradigm where all persons share the same heatmap.
            A batch_size of `num_persons` is used for the top down paradigm where each person has its own heatmaps.
        kernel (`int`, *optional*, defaults to 3):
            Gaussian kernel size (K) for modulation.

    Returns:
        `np.ndarray` of shape `(num_persons, num_keypoints, 2)` ):
            Refined coordinates.
    """
    batch_size, num_keypoints, height, width = batch_heatmaps.shape
    num_coords = coords.shape[0]
    if not (batch_size == 1 or batch_size == num_coords):
        raise ValueError("The batch size of heatmaps should be 1 or equal to the batch size of coordinates.")
    radius = int((kernel - 1) // 2)
    batch_heatmaps = np.array(
        [
            [gaussian_filter(heatmap, sigma=0.8, radius=(radius, radius), axes=(0, 1)) for heatmap in heatmaps]
            for heatmaps in batch_heatmaps
        ]
    )
    batch_heatmaps = np.clip(batch_heatmaps, 0.001, 50)
    batch_heatmaps = np.log(batch_heatmaps)

    batch_heatmaps_pad = np.pad(batch_heatmaps, ((0, 0), (0, 0), (1, 1), (1, 1)), mode="edge").flatten()
    index = coords[..., 0] + 1 + (coords[..., 1] + 1) * (width + 2)
    index += (width + 2) * (height + 2) * np.arange(0, batch_size * num_keypoints).reshape(-1, num_keypoints)
    index = index.astype(int).reshape(-1, 1)
    i_ = batch_heatmaps_pad[index]
    ix1 = batch_heatmaps_pad[index + 1]
    iy1 = batch_heatmaps_pad[index + width + 2]
    ix1y1 = batch_heatmaps_pad[index + width + 3]
    ix1_y1_ = batch_heatmaps_pad[index - width - 3]
    ix1_ = batch_heatmaps_pad[index - 1]
    iy1_ = batch_heatmaps_pad[index - 2 - width]
    dx = 0.5 * (ix1 - ix1_)
    dy = 0.5 * (iy1 - iy1_)
    derivative = np.concatenate([dx, dy], axis=1)
    derivative = derivative.reshape(num_coords, num_keypoints, 2, 1)
    dxx = ix1 - 2 * i_ + ix1_
    dyy = iy1 - 2 * i_ + iy1_
    dxy = 0.5 * (ix1y1 - ix1 - iy1 + i_ + i_ - ix1_ - iy1_ + ix1_y1_)
    hessian = np.concatenate([dxx, dxy, dxy, dyy], axis=1)
    hessian = hessian.reshape(num_coords, num_keypoints, 2, 2)
    hessian = np.linalg.inv(hessian + np.finfo(np.float32).eps * np.eye(2))
    coords -= np.einsum("ijmn,ijnk->ijmk", hessian, derivative).squeeze()
    return coords


def post_dark_unbiased_data_processing(coords: np.ndarray, batch_heatmaps: np.ndarray, kernel: int = 3) -> np.ndarray:
    """DARK post-pocessing. Implemented by unbiased_data_processing.

    Paper references:
    - Huang et al. The Devil is in the Details: Delving into Unbiased Data Processing for Human Pose Estimation (CVPR 2020).
    - Zhang et al. Distribution-Aware Coordinate Representation for Human Pose Estimation (CVPR 2020).

    Args:
        coords (`np.ndarray` of shape `(num_persons, num_keypoints, 2)`):
            Initial coordinates of human pose.
        batch_heatmaps (`np.ndarray` of shape `(batch_size, num_keypoints, height, width)`):
            Batched heatmaps as predicted by the model.
            A batch_size of 1 is used for the bottom up paradigm where all persons share the same heatmap.
            A batch_size of `num_persons` is used for the top down paradigm where each person has its own heatmaps.
        kernel (`int`, *optional*, defaults to 3):
            Gaussian kernel size (K) for modulation.

    Returns:
        `np.ndarray` of shape `(num_persons, num_keypoints, 2)` ):
            Refined coordinates.
    """
    batch_size, num_keypoints, height, width = batch_heatmaps.shape
    num_coords = coords.shape[0]
    if not (batch_size == 1 or batch_size == num_coords):
        raise ValueError("The batch size of heatmaps should be 1 or equal to the batch size of coordinates.")
    radius = int((kernel - 1) // 2)
    batch_heatmaps = np.array(
        [
            [gaussian_filter(heatmap, sigma=0.8, radius=(radius, radius), axes=(0, 1)) for heatmap in heatmaps]
            for heatmaps in batch_heatmaps
        ]
    )
    batch_heatmaps = np.clip(batch_heatmaps, 0.001, 50)
    batch_heatmaps = np.log(batch_heatmaps)

    batch_heatmaps_pad = np.pad(batch_heatmaps, ((0, 0), (0, 0), (1, 1), (1, 1)), mode="edge").flatten()
    index = coords[..., 0] + 1 + (coords[..., 1] + 1) * (width + 2)
    index += (width + 2) * (height + 2) * np.arange(0, batch_size * num_keypoints).reshape(-1, num_keypoints)
    index = index.astype(int).reshape(-1, 1)
    i_ = batch_heatmaps_pad[index]
    ix1 = batch_heatmaps_pad[index + 1]
    iy1 = batch_heatmaps_pad[index + width + 2]
    ix1y1 = batch_heatmaps_pad[index + width + 3]
    ix1_y1_ = batch_heatmaps_pad[index - width - 3]
    ix1_ = batch_heatmaps_pad[index - 1]
    iy1_ = batch_heatmaps_pad[index - 2 - width]
    dx = 0.5 * (ix1 - ix1_)
    dy = 0.5 * (iy1 - iy1_)
    derivative = np.concatenate([dx, dy], axis=1)
    derivative = derivative.reshape(num_coords, num_keypoints, 2, 1)
    dxx = ix1 - 2 * i_ + ix1_
    dyy = iy1 - 2 * i_ + iy1_
    dxy = 0.5 * (ix1y1 - ix1 - iy1 + i_ + i_ - ix1_ - iy1_ + ix1_y1_)
    hessian = np.concatenate([dxx, dxy, dxy, dyy], axis=1)
    hessian = hessian.reshape(num_coords, num_keypoints, 2, 2)
    hessian = np.linalg.inv(hessian + np.finfo(np.float32).eps * np.eye(2))
    coords -= np.einsum("ijmn,ijnk->ijmk", hessian, derivative).squeeze()
    return coords

