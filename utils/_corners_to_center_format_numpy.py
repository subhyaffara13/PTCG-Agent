
def _corners_to_center_format_numpy(bboxes_corners: np.ndarray) -> np.ndarray:
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = bboxes_corners.T
    bboxes_center = np.stack(
        [
            (top_left_x + bottom_right_x) / 2,  # center x
            (top_left_y + bottom_right_y) / 2,  # center y
            (bottom_right_x - top_left_x),  # width
            (bottom_right_y - top_left_y),  # height
        ],
        axis=-1,
    )
    return bboxes_center

