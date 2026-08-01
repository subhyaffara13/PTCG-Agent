
def is_valid_list_of_audio(audio):
    return audio and all(is_valid_audio(audio_i) for audio_i in audio)

