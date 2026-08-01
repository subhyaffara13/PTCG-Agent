
def calculate_img_tokens(
    data,
    mode: Literal["low", "high", "auto"] = "auto",
    base_tokens: int = 85,  # openai default - https://openai.com/pricing
    use_default_image_token_count: bool = False,
):
    """
    Calculate the number of tokens for an image.

    Args:
        data (str): The URL or base64 encoded string of the image.
        mode (Literal["low", "high", "auto"]): The mode to use for calculating the number of tokens.
        base_tokens (int): The base number of tokens for an image.
        use_default_image_token_count (bool): When True, will NOT make a GET request to the image URL and instead return the default image dimensions.

    Returns:
        int: The number of tokens for the image.
    """
    if use_default_image_token_count:
        verbose_logger.debug(
            "Using default image token count: {}".format(DEFAULT_IMAGE_TOKEN_COUNT)
        )
        return DEFAULT_IMAGE_TOKEN_COUNT
    if mode == "low" or mode == "auto":
        return base_tokens
    elif mode == "high":
        # Run the async function using the helper
        width, height = get_image_dimensions(
            data=data,
        )
        resized_width, resized_height = resize_image_high_res(
            width=width, height=height
        )
        tiles_needed_high_res = calculate_tiles_needed(
            resized_width=resized_width, resized_height=resized_height
        )
        tile_tokens = (base_tokens * 2) * tiles_needed_high_res
        total_tokens = base_tokens + tile_tokens
        return total_tokens

