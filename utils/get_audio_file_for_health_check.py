import os

def get_audio_file_for_health_check() -> FileTypes:
    """
    Get an audio file for health check

    Returns the content of `audio_health_check.wav` in the same directory as this file
    """
    pwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(pwd, "audio_health_check.wav")
    return open(file_path, "rb")

