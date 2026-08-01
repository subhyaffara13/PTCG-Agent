
def flip_back(output_flipped, flip_pairs, target_type="gaussian-heatmap"):
    """Flip the flipped heatmaps back to the original form.

    Args:
        output_flipped (`torch.tensor` of shape `(batch_size, num_keypoints, height, width)`):
            The output heatmaps obtained from the flipped images.
        flip_pairs (`torch.Tensor` of shape `(num_keypoints, 2)`):
            Pairs of keypoints which are mirrored (for example, left ear -- right ear).
        target_type (`str`, *optional*, defaults to `"gaussian-heatmap"`):
            Target type to use. Can be gaussian-heatmap or combined-target.
            gaussian-heatmap: Classification target with gaussian distribution.
            combined-target: The combination of classification target (response map) and regression target (offset map).
            Paper ref: Huang et al. The Devil is in the Details: Delving into Unbiased Data Processing for Human Pose Estimation (CVPR 2020).

    Returns:
        torch.Tensor: heatmaps that flipped back to the original image
    """
    if target_type not in ["gaussian-heatmap", "combined-target"]:
        raise ValueError("target_type should be gaussian-heatmap or combined-target")

    if output_flipped.ndim != 4:
        raise ValueError("output_flipped should be [batch_size, num_keypoints, height, width]")

    batch_size, num_keypoints, height, width = output_flipped.shape
    channels = 1
    if target_type == "combined-target":
        channels = 3
        output_flipped = output_flipped.clone()  # clone to avoid mutation of output_flipped argument
        output_flipped[:, 1::3, ...] = -output_flipped[:, 1::3, ...]
    output_flipped = output_flipped.reshape(batch_size, -1, channels, height, width)
    output_flipped_back = output_flipped.clone()

    # Swap left-right parts
    left_indices, right_indices = flip_pairs.unbind(-1)
    output_flipped_back[:, left_indices, ...] = output_flipped[:, right_indices, ...]
    output_flipped_back[:, right_indices, ...] = output_flipped[:, left_indices, ...]
    output_flipped_back = output_flipped_back.reshape((batch_size, num_keypoints, height, width))
    # Flip horizontally
    output_flipped_back = output_flipped_back.flip(-1)
    return output_flipped_back


def flip_back(output_flipped, flip_pairs, target_type="gaussian-heatmap"):
    """Flip the flipped heatmaps back to the original form.

    Args:
        output_flipped (`torch.tensor` of shape `(batch_size, num_keypoints, height, width)`):
            The output heatmaps obtained from the flipped images.
        flip_pairs (`torch.Tensor` of shape `(num_keypoints, 2)`):
            Pairs of keypoints which are mirrored (for example, left ear -- right ear).
        target_type (`str`, *optional*, defaults to `"gaussian-heatmap"`):
            Target type to use. Can be gaussian-heatmap or combined-target.
            gaussian-heatmap: Classification target with gaussian distribution.
            combined-target: The combination of classification target (response map) and regression target (offset map).
            Paper ref: Huang et al. The Devil is in the Details: Delving into Unbiased Data Processing for Human Pose Estimation (CVPR 2020).

    Returns:
        torch.Tensor: heatmaps that flipped back to the original image
    """
    if target_type not in ["gaussian-heatmap", "combined-target"]:
        raise ValueError("target_type should be gaussian-heatmap or combined-target")

    if output_flipped.ndim != 4:
        raise ValueError("output_flipped should be [batch_size, num_keypoints, height, width]")

    batch_size, num_keypoints, height, width = output_flipped.shape
    channels = 1
    if target_type == "combined-target":
        channels = 3
        output_flipped = output_flipped.clone()  # clone to avoid mutation of output_flipped argument
        output_flipped[:, 1::3, ...] = -output_flipped[:, 1::3, ...]
    output_flipped = output_flipped.reshape(batch_size, -1, channels, height, width)
    output_flipped_back = output_flipped.clone()

    # Swap left-right parts
    left_indices, right_indices = flip_pairs.unbind(-1)
    output_flipped_back[:, left_indices, ...] = output_flipped[:, right_indices, ...]
    output_flipped_back[:, right_indices, ...] = output_flipped[:, left_indices, ...]
    output_flipped_back = output_flipped_back.reshape((batch_size, num_keypoints, height, width))
    # Flip horizontally
    output_flipped_back = output_flipped_back.flip(-1)
    return output_flipped_back

