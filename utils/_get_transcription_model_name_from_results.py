
def _get_transcription_model_name_from_results(
    results: OpenAIRealtimeStreamList,
) -> Optional[str]:
    """Resolve the ASR model from a transcription_session.* / session.* event."""
    for result in results:
        if result.get("type") in (
            "transcription_session.created",
            "transcription_session.updated",
            "session.created",
            "session.updated",
        ):
            session = cast(dict, result).get("session", {}) or {}
            transcription = (
                (session.get("audio", {}) or {}).get("input", {}) or {}
            ).get("transcription", {}) or session.get("input_audio_transcription", {})
            model = (transcription or {}).get("model") or session.get("model")
            if model:
                return model
    return None

