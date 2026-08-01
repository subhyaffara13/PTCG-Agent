
def transform_preds(coords: np.ndarray, center: np.ndarray, scale: np.ndarray, output_size: np.ndarray) -> np.ndarray:
    """Get final keypoint predictions from heatmaps and apply scaling and
    translation to map them back to the image.

    Note:
        num_keypoints: K

    Args:
        coords (`np.ndarray` of shape `(num_keypoints, ndims)`):

            * If ndims=2, corrds are predicted keypoint location.
            * If ndims=4, corrds are composed of (x, y, scores, tags)
            * If ndims=5, corrds are composed of (x, y, scores, tags,
              flipped_tags)

        center (`np.ndarray` of shape `(2,)`):
            Center of the bounding box (x, y).
        scale (`np.ndarray` of shape `(2,)`):
            Scale of the bounding box wrt original image of width and height.
        output_size (`np.ndarray` of shape `(2,)`):
            Size of the destination heatmaps in (height, width) format.

    Returns:
        np.ndarray: Predicted coordinates in the images.
    """
    if coords.shape[1] not in (2, 4, 5):
        raise ValueError("Coordinates need to have either 2, 4 or 5 dimensions.")
    if len(center) != 2:
        raise ValueError("Center needs to have 2 elements, one for x and one for y.")
    if len(scale) != 2:
        raise ValueError("Scale needs to consist of a width and height")
    if len(output_size) != 2:
        raise ValueError("Output size needs to consist of a height and width")

    # Recover the scale which is normalized by a factor of 200.
    scale = scale * 200.0

    # We use unbiased data processing
    scale_y = scale[1] / (output_size[0] - 1.0)
    scale_x = scale[0] / (output_size[1] - 1.0)

    target_coords = np.ones_like(coords)
    target_coords[:, 0] = coords[:, 0] * scale_x + center[0] - scale[0] * 0.5
    target_coords[:, 1] = coords[:, 1] * scale_y + center[1] - scale[1] * 0.5

    return target_coords


def transform_preds(coords: np.ndarray, center: np.ndarray, scale: np.ndarray, output_size: np.ndarray) -> np.ndarray:
    """Get final keypoint predictions from heatmaps and apply scaling and
    translation to map them back to the image.

    Note:
        num_keypoints: K

    Args:
        coords (`np.ndarray` of shape `(num_keypoints, ndims)`):

            * If ndims=2, corrds are predicted keypoint location.
            * If ndims=4, corrds are composed of (x, y, scores, tags)
            * If ndims=5, corrds are composed of (x, y, scores, tags,
              flipped_tags)

        center (`np.ndarray` of shape `(2,)`):
            Center of the bounding box (x, y).
        scale (`np.ndarray` of shape `(2,)`):
            Scale of the bounding box wrt original image of width and height.
        output_size (`np.ndarray` of shape `(2,)`):
            Size of the destination heatmaps in (height, width) format.

    Returns:
        np.ndarray: Predicted coordinates in the images.
    """
    if coords.shape[1] not in (2, 4, 5):
        raise ValueError("Coordinates need to have either 2, 4 or 5 dimensions.")
    if len(center) != 2:
        raise ValueError("Center needs to have 2 elements, one for x and one for y.")
    if len(scale) != 2:
        raise ValueError("Scale needs to consist of a width and height")
    if len(output_size) != 2:
        raise ValueError("Output size needs to consist of a height and width")

    # Recover the scale which is normalized by a factor of 200.
    scale = scale * 200.0

    # We use unbiased data processing
    scale_y = scale[1] / (output_size[0] - 1.0)
    scale_x = scale[0] / (output_size[1] - 1.0)

    target_coords = np.ones_like(coords)
    target_coords[:, 0] = coords[:, 0] * scale_x + center[0] - scale[0] * 0.5
    target_coords[:, 1] = coords[:, 1] * scale_y + center[1] - scale[1] * 0.5

    return target_coords

