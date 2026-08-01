
def render_text(
    text: str,
    text_size: int = 36,
    text_color: str = "black",
    background_color: str = "white",
    left_padding: int = 5,
    right_padding: int = 5,
    top_padding: int = 5,
    bottom_padding: int = 5,
    font_bytes: bytes | None = None,
    font_path: str | None = None,
) -> Image.Image:
    """
    Render text. This script is entirely adapted from the original script that can be found here:
    https://github.com/google-research/pix2struct/blob/main/pix2struct/preprocessing/preprocessing_utils.py

    Args:
        text (`str`, *optional*, defaults to ):
            Text to render.
        text_size (`int`, *optional*, defaults to 36):
            Size of the text.
        text_color (`str`, *optional*, defaults to `"black"`):
            Color of the text.
        background_color (`str`, *optional*, defaults to `"white"`):
            Color of the background.
        left_padding (`int`, *optional*, defaults to 5):
            Padding on the left.
        right_padding (`int`, *optional*, defaults to 5):
            Padding on the right.
        top_padding (`int`, *optional*, defaults to 5):
            Padding on the top.
        bottom_padding (`int`, *optional*, defaults to 5):
            Padding on the bottom.
        font_bytes (`bytes`, *optional*):
            Bytes of the font to use. If `None`, the default font will be used.
        font_path (`str`, *optional*):
            Path to the font to use. If `None`, the default font will be used.
    """
    requires_backends(render_text, "vision")
    # Add new lines so that each line is no more than 80 characters.

    wrapper = textwrap.TextWrapper(width=80)
    lines = wrapper.wrap(text=text)
    wrapped_text = "\n".join(lines)

    if font_bytes is not None and font_path is None:
        font = io.BytesIO(font_bytes)
    elif font_path is not None:
        font = font_path
    else:
        font = hf_api().hf_hub_download(DEFAULT_FONT_PATH, "Arial.TTF")
    font = ImageFont.truetype(font, encoding="UTF-8", size=text_size)

    # Use a temporary canvas to determine the width and height in pixels when
    # rendering the text.
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    _, _, w, h = temp_draw.textbbox((0, 0), wrapped_text, font=font)

    text_width = w + left_padding + right_padding
    text_height = h + top_padding + bottom_padding

    # Create the actual image with the text.
    img = Image.new("RGB", (text_width, text_height), background_color)
    draw = ImageDraw.Draw(img)
    draw.text((left_padding, top_padding), wrapped_text, fill=text_color, font=font)

    return img


def render_text(
    text: str,
    text_size: int = 36,
    text_color: str = "black",
    background_color: str = "white",
    left_padding: int = 5,
    right_padding: int = 5,
    top_padding: int = 5,
    bottom_padding: int = 5,
    font_bytes: bytes | None = None,
    font_path: str | None = None,
) -> Image.Image:
    """
    Render text. This script is entirely adapted from the original script that can be found here:
    https://github.com/google-research/pix2struct/blob/main/pix2struct/preprocessing/preprocessing_utils.py

    Args:
        text (`str`, *optional*, defaults to ):
            Text to render.
        text_size (`int`, *optional*, defaults to 36):
            Size of the text.
        text_color (`str`, *optional*, defaults to `"black"`):
            Color of the text.
        background_color (`str`, *optional*, defaults to `"white"`):
            Color of the background.
        left_padding (`int`, *optional*, defaults to 5):
            Padding on the left.
        right_padding (`int`, *optional*, defaults to 5):
            Padding on the right.
        top_padding (`int`, *optional*, defaults to 5):
            Padding on the top.
        bottom_padding (`int`, *optional*, defaults to 5):
            Padding on the bottom.
        font_bytes (`bytes`, *optional*):
            Bytes of the font to use. If `None`, the default font will be used.
        font_path (`str`, *optional*):
            Path to the font to use. If `None`, the default font will be used.
    """
    requires_backends(render_text, "vision")
    # Add new lines so that each line is no more than 80 characters.

    wrapper = textwrap.TextWrapper(width=80)
    lines = wrapper.wrap(text=text)
    wrapped_text = "\n".join(lines)

    if font_bytes is not None and font_path is None:
        font = io.BytesIO(font_bytes)
    elif font_path is not None:
        font = font_path
    else:
        font = hf_api().hf_hub_download(DEFAULT_FONT_PATH, "Arial.TTF")
    font = ImageFont.truetype(font, encoding="UTF-8", size=text_size)

    # Use a temporary canvas to determine the width and height in pixels when
    # rendering the text.
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    _, _, w, h = temp_draw.textbbox((0, 0), wrapped_text, font=font)

    text_width = w + left_padding + right_padding
    text_height = h + top_padding + bottom_padding

    # Create the actual image with the text.
    img = Image.new("RGB", (text_width, text_height), background_color)
    draw = ImageDraw.Draw(img)
    draw.text((left_padding, top_padding), wrapped_text, fill=text_color, font=font)

    return img

