
def load_audio(audio: str | np.ndarray, sampling_rate=16000, timeout=None) -> np.ndarray:
    """
    Loads `audio` to an np.ndarray object.

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
    if isinstance(audio, str):
        # Try to load with `torchcodec` but do not enforce users to install it. If not found
        # fallback to `librosa`. If using an audio-only model, most probably `torchcodec` won't be
        # needed. Do not raise any errors if not installed or versions do not match
        if is_torchcodec_available() and version.parse("0.3.0") <= TORCHCODEC_VERSION:
            audio = load_audio_torchcodec(audio, sampling_rate=sampling_rate, timeout=timeout)
        elif audio.rsplit("?", 1)[0].lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv")):
            raise RuntimeError(
                f"The audio source appears to be a video file ('{audio.split('/')[-1]}'). "
                "librosa cannot decode video containers. "
                "Install torchcodec>=0.3.0 (`pip install torchcodec`) to load audio from video files."
            )
        else:
            audio = load_audio_librosa(audio, sampling_rate=sampling_rate, timeout=timeout)
    elif not isinstance(audio, np.ndarray):
        raise TypeError(
            "Incorrect format used for `audio`. Should be an url linking to an audio, a local path, or numpy array."
        )
    return audio

