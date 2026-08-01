
def audio(tag, tensor, sample_rate=44100):
    array = make_np(tensor)
    array = array.squeeze()
    if abs(array).max() > 1:
        print("warning: audio amplitude out of range, auto clipped.")
        array = array.clip(-1, 1)
    if array.ndim != 1:
        raise AssertionError("input tensor should be 1 dimensional.")
    # pyrefly: ignore [no-matching-overload]
    array = (array * np.iinfo(np.int16).max).astype("<i2")

    import io
    import wave

    fio = io.BytesIO()
    with wave.open(fio, "wb") as wave_write:
        wave_write.setnchannels(1)
        wave_write.setsampwidth(2)
        wave_write.setframerate(sample_rate)
        wave_write.writeframes(array.data)
    audio_string = fio.getvalue()
    fio.close()
    audio = Summary.Audio(
        sample_rate=sample_rate,
        num_channels=1,
        length_frames=array.shape[-1],
        encoded_audio_string=audio_string,
        content_type="audio/wav",
    )
    return Summary(value=[Summary.Value(tag=tag, audio=audio)])

