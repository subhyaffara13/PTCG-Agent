
def convert_generic_image_chunk_to_openai_image_obj(
    image_chunk: GenericImageParsingChunk,
) -> str:
    """
    Convert a generic image chunk to an OpenAI image object.

    Input:
    GenericImageParsingChunk(
        type="base64",
        media_type="image/jpeg",
        data="...",
    )

    Return:
    "data:image/jpeg;base64,{base64_image}"
    """
    media_type = image_chunk["media_type"]
    return "data:{};{},{}".format(media_type, image_chunk["type"], image_chunk["data"])

