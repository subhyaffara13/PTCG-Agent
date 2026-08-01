
def _group_tokens_into_cues(
    tokens: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Group Soniox tokens into subtitle cues.

    Each cue has:
      - start_ms: int
      - end_ms: int
      - text: str

    Grouping heuristics:
      - A new cue starts when token count exceeds _CUE_MAX_TOKENS.
      - A new cue starts when duration exceeds _CUE_MAX_DURATION_MS.
      - A new cue starts when the speaker changes (if diarization is on).
      - Tokens without timestamps are appended to the current cue.
    """
    cues: List[Dict[str, Any]] = []
    current_tokens: List[str] = []
    current_start: Optional[int] = None
    current_end: Optional[int] = None
    current_speaker: Optional[Any] = None

    def _flush() -> None:
        if current_tokens and current_start is not None:
            text = "".join(current_tokens).strip()
            if text:
                cues.append(
                    {
                        "start_ms": current_start,
                        "end_ms": (
                            current_end if current_end is not None else current_start
                        ),
                        "text": text,
                    }
                )

    for token in tokens:
        start_ms = token.get("start_ms")
        end_ms = token.get("end_ms")
        text = token.get("text", "")
        speaker = token.get("speaker")

        # Skip tokens with no timestamp data entirely if we have no cue started
        if start_ms is None and current_start is None:
            continue

        # Speaker change forces a new cue
        if speaker is not None and speaker != current_speaker:
            _flush()
            current_tokens = []
            current_start = start_ms
            current_end = end_ms
            current_speaker = speaker
            current_tokens.append(text)
            continue

        # Duration or token count exceeded -> flush
        should_break = False
        if len(current_tokens) >= _CUE_MAX_TOKENS:
            should_break = True
        elif (
            current_start is not None
            and start_ms is not None
            and (start_ms - current_start) >= _CUE_MAX_DURATION_MS
        ):
            should_break = True

        if should_break:
            _flush()
            current_tokens = []
            current_start = start_ms
            current_end = end_ms
            current_tokens.append(text)
        else:
            if current_start is None:
                current_start = start_ms
            if end_ms is not None:
                current_end = end_ms
            current_tokens.append(text)

    _flush()
    return cues

