
def is_valid_image(img):
    return is_pil_image(img) or is_numpy_array(img) or is_torch_tensor(img)

