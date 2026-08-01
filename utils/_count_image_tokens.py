
def _count_image_tokens(
    image_url: Any,
    use_default_image_token_count: bool,
) -> int:
    """
    Count tokens for an image_url content block.

    Args:
        image_url: The image URL data - can be a string URL or dict with 'url' and 'detail'
        use_default_image_token_count: Whether to use default image token counts

    Returns:
        int: Number of tokens for the image

    Raises:
        ValueError: If image_url is invalid type or detail value is invalid
    """
    if isinstance(image_url, dict):
        detail = image_url.get("detail", "auto")
        if detail not in ["low", "high", "auto"]:
            raise ValueError(
                f"Invalid detail value: {detail}. Expected 'low', 'high', or 'auto'."
            )
        url = image_url.get("url")
        if not url:
            raise ValueError("Missing required key 'url' in image_url dict.")
        return calculate_img_tokens(
            data=url,
            mode=detail,  # type: ignore
            use_default_image_token_count=use_default_image_token_count,
        )
    elif isinstance(image_url, str):
        if not image_url.strip():
            raise ValueError("Empty image_url string is not valid.")
        return calculate_img_tokens(
            data=image_url,
            mode="auto",
            use_default_image_token_count=use_default_image_token_count,
        )
    else:
        raise ValueError(
            f"Invalid image_url type: {type(image_url).__name__}. "
            "Expected str or dict with 'url' field."
        )

