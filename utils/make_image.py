
def make_image(tensor, rescale=1, rois=None, labels=None):
    """Convert a numpy representation of an image to Image protobuf."""
    from PIL import Image

    height, width, channel = tensor.shape
    scaled_height = int(height * rescale)
    scaled_width = int(width * rescale)
    image = Image.fromarray(tensor)
    if rois is not None:
        image = draw_boxes(image, rois, labels=labels)
    ANTIALIAS = Image.Resampling.LANCZOS
    image = image.resize((scaled_width, scaled_height), ANTIALIAS)
    import io

    output = io.BytesIO()
    image.save(output, format="PNG")
    image_string = output.getvalue()
    output.close()
    return Summary.Image(
        height=height,
        width=width,
        colorspace=channel,
        encoded_image_string=image_string,
    )

