
def extract_duration_from_srt_or_vtt(srt_or_vtt_content: str) -> Optional[float]:
    """
    Extracts the total duration (in seconds) from SRT or VTT content.

    Args:
        srt_or_vtt_content (str): The content of an SRT or VTT file as a string.

    Returns:
        Optional[float]: The total duration in seconds, or None if no timestamps are found.
    """
    # Regular expression to match timestamps in the format "hh:mm:ss,ms" or "hh:mm:ss.ms"
    timestamp_pattern = r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})"

    timestamps = re.findall(timestamp_pattern, srt_or_vtt_content)

    if not timestamps:
        return None

    # Convert timestamps to seconds and find the max (end time)
    durations = []
    for match in timestamps:
        hours, minutes, seconds, milliseconds = map(int, match)
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        durations.append(total_seconds)

    return max(durations) if durations else None

