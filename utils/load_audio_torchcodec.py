
def load_audio_torchcodec(audio: str | np.ndarray, sampling_rate=16000, timeout=None) -> np.ndarray:
    """
    Loads `audio` to an np.ndarray object using `torchcodec`.

    Args:
        audio (`str` or `np.ndarray`):
            The audio to be loaded to the numpy array format.
        sampling_rate (`int`, *optional*, defaults to 16000):
            The sampling rate to be used when loading the audio. It should be same as the
            sampling rate the model you will be using further was trained with.
        timeout (`float`, *optional*):
            The timeout value in seconds for the URL request.

    Returns:
        `np.ndarray`: A numpy array representing the audio.
    """
    # Lazy import so that issues in torchcodec compatibility don't crash the whole library
    requires_backends(load_audio_torchcodec, ["torchcodec"])
    from torchcodec.decoders import AudioDecoder

    # Fetch bytes for URLs so we get retry logic; torchcodec does not surface ffmpeg network retries options
    if isinstance(audio, str) and audio.startswith(("http://", "https://")):
        audio = _fetch_audio_bytes(audio, timeout=timeout)

    # Set `num_channels` to `1` which is what most models expects and the default in librosa
    decoder = AudioDecoder(audio, sample_rate=sampling_rate, num_channels=1)
    audio = decoder.get_all_samples().data[0].numpy()  # NOTE: feature extractors don't accept torch tensors
    return audio

