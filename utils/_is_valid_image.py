
def _is_valid_image(image):
    return is_pil_image(image) or (
        is_valid_image(image) and get_image_type(image) != ImageType.PIL and len(image.shape) == 3
    )


def _is_valid_image(image):
    return is_pil_image(image) or (
        is_valid_image(image) and get_image_type(image) != ImageType.PIL and len(image.shape) == 3
    )


def _is_valid_image(image):
    return is_pil_image(image) or (
        is_valid_image(image) and get_image_type(image) != ImageType.PIL and len(image.shape) == 3
    )

