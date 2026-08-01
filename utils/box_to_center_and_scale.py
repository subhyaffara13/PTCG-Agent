
def box_to_center_and_scale(
    box: tuple | list | np.ndarray,
    image_width: int,
    image_height: int,
    normalize_factor: float = 200.0,
    padding_factor: float = 1.25,
):
    """
    Encodes a bounding box in COCO format into (center, scale).

    Args:
        box (`Tuple`, `List`, or `np.ndarray`):
            Bounding box in COCO format (top_left_x, top_left_y, width, height).
        image_width (`int`):
            Image width.
        image_height (`int`):
            Image height.
        normalize_factor (`float`):
            Width and height scale factor.
        padding_factor (`float`):
            Bounding box padding factor.

    Returns:
        tuple: A tuple containing center and scale.

        - `np.ndarray` [float32](2,): Center of the bbox (x, y).
        - `np.ndarray` [float32](2,): Scale of the bbox width & height.
    """

    top_left_x, top_left_y, width, height = box[:4]
    aspect_ratio = image_width / image_height
    center = np.array([top_left_x + width * 0.5, top_left_y + height * 0.5], dtype=np.float32)

    if width > aspect_ratio * height:
        height = width * 1.0 / aspect_ratio
    elif width < aspect_ratio * height:
        width = height * aspect_ratio

    scale = np.array([width / normalize_factor, height / normalize_factor], dtype=np.float32)
    scale = scale * padding_factor

    return center, scale


def box_to_center_and_scale(
    box: tuple | list | np.ndarray,
    image_width: int,
    image_height: int,
    normalize_factor: float = 200.0,
    padding_factor: float = 1.25,
):
    """
    Encodes a bounding box in COCO format into (center, scale).

    Args:
        box (`Tuple`, `List`, or `np.ndarray`):
            Bounding box in COCO format (top_left_x, top_left_y, width, height).
        image_width (`int`):
            Image width.
        image_height (`int`):
            Image height.
        normalize_factor (`float`):
            Width and height scale factor.
        padding_factor (`float`):
            Bounding box padding factor.

    Returns:
        tuple: A tuple containing center and scale.

        - `np.ndarray` [float32](2,): Center of the bbox (x, y).
        - `np.ndarray` [float32](2,): Scale of the bbox width & height.
    """

    top_left_x, top_left_y, width, height = box[:4]
    aspect_ratio = image_width / image_height
    center = np.array([top_left_x + width * 0.5, top_left_y + height * 0.5], dtype=np.float32)

    if width > aspect_ratio * height:
        height = width * 1.0 / aspect_ratio
    elif width < aspect_ratio * height:
        width = height * aspect_ratio

    scale = np.array([width / normalize_factor, height / normalize_factor], dtype=np.float32)
    scale = scale * padding_factor

    return center, scale

