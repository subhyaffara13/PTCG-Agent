
def center_to_corners_format(bboxes_center: TensorType) -> TensorType:
    """
    Converts bounding boxes from center format to corners format.

    center format: contains the coordinate for the center of the box and its width, height dimensions
        (center_x, center_y, width, height)
    corners format: contains the coordinates for the top-left and bottom-right corners of the box
        (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    """
    # Function is used during model forward pass, so we use torch if relevant, without converting to numpy
    if is_torch_tensor(bboxes_center):
        return _center_to_corners_format_torch(bboxes_center)
    elif isinstance(bboxes_center, np.ndarray):
        return _center_to_corners_format_numpy(bboxes_center)

    raise ValueError(f"Unsupported input type {type(bboxes_center)}")

