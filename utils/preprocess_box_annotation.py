
def preprocess_box_annotation(box: list | tuple, image_size: tuple[int, int]) -> list:
    """
    Convert box annotation to the format [x1, y1, x2, y2] in the range [0, 1000].
    """
    width, height = image_size
    if len(box) == 4:
        box[0] = int(box[0] / width * 1000)
        box[1] = int(box[1] / height * 1000)
        box[2] = int(box[2] / width * 1000)
        box[3] = int(box[3] / height * 1000)
    else:
        raise ValueError("Box must be a list or tuple of lists in the form [x1, y1, x2, y2].")

    return list(box)

