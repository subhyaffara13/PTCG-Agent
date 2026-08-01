
def is_valid_audio(audio):
    return (
        is_numpy_array(audio)
        or is_torch_tensor(audio)
        or (isinstance(audio, (list, tuple)) and isinstance(audio[0], float))
    )

