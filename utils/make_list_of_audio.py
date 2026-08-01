
def make_list_of_audio(
    audio: list[AudioInput] | AudioInput,
) -> AudioInput:
    """
    Ensure that the output is a list of audio.
    Args:
        audio (`Union[list[AudioInput], AudioInput]`):
            The input audio.
    Returns:
        list: A list of audio.
    """
    # If it's a list of audios, it's already in the right format
    if isinstance(audio, (list, tuple)) and is_valid_list_of_audio(audio):
        return audio

    # If it's a single audio, convert it to a list of
    if is_valid_audio(audio):
        return [audio]

    raise ValueError("Invalid input type. Must be a single audio or a list of audio")

