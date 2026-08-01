
def handle_realtime_transcription_cost_calculation(
    results: OpenAIRealtimeStreamList,
    custom_llm_provider: str,
    litellm_model_name: str,
) -> float:
    """
    Cost for realtime transcription sessions (e.g. gpt-realtime-whisper).

    Transcription sessions emit no `response.done` events; instead each
    `conversation.item.input_audio_transcription.completed` event carries a
    `usage` object billed by the ASR model. The usage is one of:
      - {"type": "duration", "seconds": <float>}  → priced via input_cost_per_second
      - {"type": "tokens", "input_tokens": ...}    → priced via input/audio token cost
    """
    completed_events = [
        cast(dict, result)
        for result in results
        if result.get("type") == _TRANSCRIPTION_COMPLETED_EVENT_TYPE
    ]
    if not completed_events:
        return 0.0

    model_name = (
        _get_transcription_model_name_from_results(results) or litellm_model_name
    )
    try:
        model_info = litellm.get_model_info(
            model=model_name, custom_llm_provider=custom_llm_provider
        )
    except Exception:
        model_info = None

    total_cost = 0.0
    for event in completed_events:
        usage = event.get("usage") or {}
        total_cost += _transcription_usage_cost(usage, model_info)
    return total_cost

