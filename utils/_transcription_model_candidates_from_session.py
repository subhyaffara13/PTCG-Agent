
def _transcription_model_candidates_from_session(session: dict) -> list[str]:
    candidates: list[str] = []

    audio = session.get("audio")
    if isinstance(audio, dict):
        audio_input = audio.get("input")
        if isinstance(audio_input, dict):
            nested_transcription = audio_input.get("transcription")
            if isinstance(nested_transcription, dict):
                _append_model_candidate(
                    candidates,
                    nested_transcription.get("model"),
                )

    flat_transcription = session.get("input_audio_transcription")
    if isinstance(flat_transcription, dict):
        _append_model_candidate(candidates, flat_transcription.get("model"))

    return candidates

