
def _load_image_from_url(image_url):
    try:
        from PIL import Image
    except Exception:
        raise Exception("image conversion failed please run `pip install Pillow`")
    from io import BytesIO

    try:
        # Send a GET request to the image URL
        client = HTTPHandler(concurrent_limit=1)
        response = safe_get(client, image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check the response's content type to ensure it is an image
        content_type = response.headers.get("content-type")
        if not content_type or "image" not in content_type:
            raise ValueError(
                f"URL does not point to a valid image (content-type: {content_type})"
            )

        # Load the image from the response content
        return Image.open(BytesIO(response.content))

    except Exception as e:
        raise e

