
def render_soniox_tokens_as_vtt(tokens: List[Dict[str, Any]]) -> str:
    """
    Render Soniox tokens as WebVTT subtitle format.

    Returns the VTT header even if no cues are present.
    """
    cues = _group_tokens_into_cues(tokens)

    lines: List[str] = ["WEBVTT", ""]
    for cue in cues:
        start = _format_timestamp_vtt(cue["start_ms"])
        end = _format_timestamp_vtt(cue["end_ms"])
        lines.append(f"{start} --> {end}")
        lines.append(cue["text"])
        lines.append("")  # blank line between cues

    return "\n".join(lines)

