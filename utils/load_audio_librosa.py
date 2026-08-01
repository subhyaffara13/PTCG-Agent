
def load_audio_librosa(audio: str | np.ndarray, sampling_rate=16000, timeout=None) -> np.ndarray:
    """
    Loads `audio` to an np.ndarray object using `librosa`.

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
    requires_backends(load_audio_librosa, ["librosa"])

    # Load audio from URL (e.g https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen2-Audio/audio/translate_to_chinese.wav)
    if audio.startswith("http://") or audio.startswith("https://"):
        audio = librosa.load(BytesIO(_fetch_audio_bytes(audio, timeout=timeout)), sr=sampling_rate)[0]
    elif os.path.isfile(audio):
        audio = librosa.load(audio, sr=sampling_rate)[0]
    return audio

