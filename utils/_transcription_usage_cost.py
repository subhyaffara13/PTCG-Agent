
def _transcription_usage_cost(usage: dict, model_info: Optional[ModelInfo]) -> float:
    if model_info is None:
        return 0.0
    usage_type = usage.get("type")
    if usage_type == "duration":
        seconds = usage.get("seconds") or 0.0
        per_second = model_info.get("input_cost_per_second") or 0.0
        return float(seconds) * float(per_second)
    if usage_type == "tokens":
        input_token_details = usage.get("input_token_details") or {}
        audio_tokens = input_token_details.get("audio_tokens") or 0
        text_tokens = input_token_details.get("text_tokens") or 0
        output_tokens = usage.get("output_tokens") or 0
        audio_cost = float(audio_tokens) * float(
            model_info.get("input_cost_per_audio_token")
            or model_info.get("input_cost_per_token")
            or 0.0
        )
        text_cost = float(text_tokens) * float(
            model_info.get("input_cost_per_token") or 0.0
        )
        output_cost = float(output_tokens) * float(
            model_info.get("output_cost_per_token") or 0.0
        )
        return audio_cost + text_cost + output_cost
    return 0.0

