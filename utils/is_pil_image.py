
def is_pil_image(img):
    return is_vision_available() and isinstance(img, PIL.Image.Image)

