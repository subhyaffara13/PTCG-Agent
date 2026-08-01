
def _load_image(path):
    img = Image.open(path)
    # In an RGBA image, if the smallest value in the alpha channel is 255, all
    # values in it must be 255, meaning that the image is opaque. If so,
    # discard the alpha channel so that it may compare equal to an RGB image.
    if img.mode != "RGBA" or img.getextrema()[3][0] == 255:
        img = img.convert("RGB")
    return np.asarray(img)

