
def render_soniox_tokens_as_srt(tokens: List[Dict[str, Any]]) -> str:
    """
    Render Soniox tokens as SRT (SubRip) subtitle format.

    Returns an empty string if no tokens have timestamp data.
    """
    cues = _group_tokens_into_cues(tokens)
    if not cues:
        return ""

    lines: List[str] = []
    for idx, cue in enumerate(cues, start=1):
        start = _format_timestamp_srt(cue["start_ms"])
        end = _format_timestamp_srt(cue["end_ms"])
        lines.append(str(idx))
        lines.append(f"{start} --> {end}")
        lines.append(cue["text"])
        lines.append("")  # blank line between cues

    return "\n".join(lines)

