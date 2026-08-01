
def resample_to_riva_pcm(file_bytes: bytes) -> ResampledAudio:
    """
    Decode ``file_bytes`` and produce 16 kHz mono LINEAR_PCM (int16 little
    endian) suitable for streaming to Riva, plus the audio duration in
    seconds (used for cost calculation when Riva does not return usage).
    """
    try:
        import numpy as np  # type: ignore
    except ImportError as e:
        raise NvidiaRivaException(
            status_code=500,
            message=f"numpy is required for Riva audio resampling. {_INSTALL_HINT}",
        ) from e

    samples_float, source_rate = _decode_to_float32(file_bytes)

    # Downmix to mono by averaging channels.
    if samples_float.ndim == 2 and samples_float.shape[1] > 1:
        samples_float = samples_float.mean(axis=1)
    elif samples_float.ndim == 2:
        samples_float = samples_float[:, 0]

    samples_float = np.asarray(samples_float, dtype=np.float32).ravel()

    if source_rate != RIVA_TARGET_SAMPLE_RATE_HZ:
        samples_float = _resample(
            samples_float, source_rate, RIVA_TARGET_SAMPLE_RATE_HZ
        )

    # Clip + convert float [-1, 1] to int16 little-endian PCM.
    np.clip(samples_float, -1.0, 1.0, out=samples_float)
    pcm_int16 = (samples_float * 32767.0).astype("<i2")
    pcm_bytes = pcm_int16.tobytes()

    duration_seconds = float(pcm_int16.size) / float(RIVA_TARGET_SAMPLE_RATE_HZ)

    return ResampledAudio(
        pcm_bytes=pcm_bytes,
        duration_seconds=duration_seconds,
        sample_rate_hz=RIVA_TARGET_SAMPLE_RATE_HZ,
        num_channels=RIVA_TARGET_NUM_CHANNELS,
    )

