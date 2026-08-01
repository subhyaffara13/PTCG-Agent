
def build_string_from_input(prompt, bos_token, image_seq_len, image_token, num_images):
    """
    Builds a string from the input prompt and image tokens.
    For example, for the call:
    build_string_from_input(
        prompt="Prefix str"
        bos_token="<s>",
        image_seq_len=3,
        image_token="<im>",
    )
    The output will be:
    "<im><im><im><s>Initial str"
    Args:
        prompt (`list[Union[str, ImageInput]]`): The input prompt.
        bos_token (`str`): The beginning of sentence token.
        image_seq_len (`int`): The length of the image sequence.
        image_token (`str`): The image token.
        num_images (`int`): Number of images in the prompt.
    """
    return f"{image_token * image_seq_len * num_images}{bos_token}{prompt}\n"


def build_string_from_input(prompt: str, bos_token: str, image_token: str) -> str:
    """
    Builds a string from the input prompt by adding `bos_token` if not already present.

    Args:
        prompt (`str`):
            The input prompt string.
        bos_token (`str`):
            The beginning of sentence token to be added.
        image_token (`str`):
            The image token used to identify the start of an image sequence.

    Returns:
        str: The modified prompt string with the `bos_token` added if necessary.

    Examples:
        >>> build_string_from_input("Hello world", "<begin_of_text>", "<|image|>")
        '<begin_of_text>Hello world'

        >>> build_string_from_input("<|image|>Hello world", "<begin_of_text>", "<|image|>")
        '<|image|><begin_of_text>Hello world'

        >>> build_string_from_input("<begin_of_text>Hello world", "<begin_of_text>", "<|image|>")
        '<begin_of_text>Hello world'
    """

    if bos_token in prompt:
        return prompt

    num_image_tokens_on_start = 0
    while prompt.startswith(image_token):
        prompt = prompt[len(image_token) :]
        num_image_tokens_on_start += 1

    return f"{image_token * num_image_tokens_on_start}{bos_token}{prompt}"


def build_string_from_input(prompt, bos_token, image_seq_len, image_token, num_images):
    """
    Builds a string from the input prompt and image tokens.
    For example, for the call:
    build_string_from_input(
        prompt="Prefix str"
        bos_token="<s>",
        image_seq_len=3,
        image_token="<im>",
    )
    The output will be:
    "<im><im><im><s>Initial str"
    Args:
        prompt (`list[Union[str, ImageInput]]`): The input prompt.
        bos_token (`str`): The beginning of sentence token.
        image_seq_len (`int`): The length of the image sequence.
        image_token (`str`): The image token.
        num_images (`int`): Number of images in the prompt.
    """
    return f"{image_token * image_seq_len * num_images}{bos_token}{prompt}\n"

