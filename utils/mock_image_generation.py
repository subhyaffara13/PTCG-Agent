
def mock_image_generation(model: str, mock_response: str):
    return ImageResponse(
        data=[ImageObject(url=mock_response)],
    )

