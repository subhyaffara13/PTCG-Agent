
def make_list_of_list_of_images(
    images: list[list[ImageInput]] | list[ImageInput] | ImageInput,
) -> list[list[ImageInput]]:
    if is_valid_image(images):
        return [[images]]

    if isinstance(images, list) and all(isinstance(image, list) for image in images):
        return images

    if isinstance(images, list):
        return [make_list_of_images(image) for image in images]

    raise ValueError("images must be a list of list of images or a list of images or an image.")


def make_list_of_list_of_images(
    images: list[list[ImageInput]] | list[ImageInput] | ImageInput,
) -> list[list[ImageInput]]:
    if is_valid_image(images):
        return [[images]]

    if isinstance(images, list) and all(isinstance(image, list) for image in images):
        return images

    if isinstance(images, list):
        return [make_list_of_images(image) for image in images]

    raise ValueError("images must be a list of list of images or a list of images or an image.")

