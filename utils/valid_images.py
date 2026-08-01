
def valid_images(imgs):
    # If we have an list of images, make sure every image is valid
    if isinstance(imgs, (list, tuple)):
        for img in imgs:
            if not valid_images(img):
                return False
    # If not a list of tuple, we have been given a single image or batched tensor of images
    elif not is_valid_image(imgs):
        return False
    return True

