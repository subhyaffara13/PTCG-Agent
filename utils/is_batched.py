
def is_batched(img):
    if isinstance(img, (list, tuple)):
        return is_valid_image(img[0])
    return False

