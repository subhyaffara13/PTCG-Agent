
def _set_transcription_model_on_session(
    session: dict,
    model: str,
    create_if_missing: bool = False,
) -> None:
    updated_existing_config = False

    flat_transcription = session.get("input_audio_transcription")
    if isinstance(flat_transcription, dict):
        session["input_audio_transcription"] = {
            **flat_transcription,
            "model": model,
        }
        updated_existing_config = True

    audio = session.get("audio")
    if isinstance(audio, dict):
        audio_input = audio.get("input")
        if isinstance(audio_input, dict):
            nested_transcription = audio_input.get("transcription")
            if isinstance(nested_transcription, dict):
                session["audio"] = {
                    **audio,
                    "input": {
                        **audio_input,
                        "transcription": {
                            **nested_transcription,
                            "model": model,
                        },
                    },
                }
                updated_existing_config = True

    if updated_existing_config or not create_if_missing:
        return

    audio = audio if isinstance(audio, dict) else {}
    audio_input = audio.get("input")
    audio_input = audio_input if isinstance(audio_input, dict) else {}
    session["audio"] = {
        **audio,
        "input": {
            **audio_input,
            "transcription": {"model": model},
        },
    }

