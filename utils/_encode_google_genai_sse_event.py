from typing import List

def _encode_google_genai_sse_event(event_lines: List[str]) -> bytes:
    return ("\n".join(event_lines) + "\n\n").encode("utf-8")

