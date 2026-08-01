
def is_valid_list_of_images(images: list):
    return images and all(is_valid_image(image) for image in images)

