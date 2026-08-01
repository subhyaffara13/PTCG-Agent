
def get_canny_image():
    import cv2  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415

    # Test Image can be downloaded from https://hf.co/datasets/huggingface/documentation-images/resolve/main/diffusers/input_image_vermeer.png
    image = Image.open("input_image_vermeer.png").convert("RGB")

    image = np.array(image)
    image = cv2.Canny(image, 100, 200)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    return Image.fromarray(image)


def get_canny_image(image) -> Image.Image:
    """
    Create canny image for SDXL control net.
    """
    image = np.array(image)
    image = cv2.Canny(image, 100, 200)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    image = Image.fromarray(image)
    return image

