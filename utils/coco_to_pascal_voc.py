
def coco_to_pascal_voc(bboxes: np.ndarray) -> np.ndarray:
    """
    Converts bounding boxes from the COCO format to the Pascal VOC format.

    In other words, converts from (top_left_x, top_left_y, width, height) format
    to (top_left_x, top_left_y, bottom_right_x, bottom_right_y).

    Args:
        bboxes (`np.ndarray` of shape `(batch_size, 4)):
            Bounding boxes in COCO format.

    Returns:
        `np.ndarray` of shape `(batch_size, 4) in Pascal VOC format.
    """
    bboxes[:, 2] = bboxes[:, 2] + bboxes[:, 0] - 1
    bboxes[:, 3] = bboxes[:, 3] + bboxes[:, 1] - 1

    return bboxes


def coco_to_pascal_voc(bboxes: np.ndarray) -> np.ndarray:
    """
    Converts bounding boxes from the COCO format to the Pascal VOC format.

    In other words, converts from (top_left_x, top_left_y, width, height) format
    to (top_left_x, top_left_y, bottom_right_x, bottom_right_y).

    Args:
        bboxes (`np.ndarray` of shape `(batch_size, 4)):
            Bounding boxes in COCO format.

    Returns:
        `np.ndarray` of shape `(batch_size, 4) in Pascal VOC format.
    """
    bboxes[:, 2] = bboxes[:, 2] + bboxes[:, 0] - 1
    bboxes[:, 3] = bboxes[:, 3] + bboxes[:, 1] - 1

    return bboxes

