
def convert_to_anthropic_image_obj(
    openai_image_url: str, format: Optional[str]
) -> GenericImageParsingChunk:
    """
    Input:
    "image_url": "data:image/jpeg;base64,{base64_image}",

    Return:
    "source": {
      "type": "base64",
      "media_type": "image/jpeg",
      "data": {base64_image},
    }
    """
    try:
        if openai_image_url.startswith("http"):
            openai_image_url = convert_url_to_base64(url=openai_image_url)
        # Extract the media type and base64 data
        media_type, base64_data = openai_image_url.split("data:")[1].split(";base64,")

        if format:
            media_type = format
        else:
            media_type = media_type.replace("\\/", "/")

        return GenericImageParsingChunk(
            type="base64",
            media_type=media_type,
            data=base64_data,
        )
    except litellm.ImageFetchError:
        raise
    except Exception as e:
        raise Exception(
            f"""Image url not in expected format. Example Expected input - "image_url": "data:image/jpeg;base64,{{base64_image}}". Supported formats - ['image/jpeg', 'image/png', 'image/gif', 'image/webp']. Error: {str(e)}"""
        )

