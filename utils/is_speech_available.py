
def is_speech_available() -> bool:
    # For now this depends on torchaudio but the exact dependency might evolve in the future.
    return is_torchaudio_available()

