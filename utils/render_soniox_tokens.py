from typing import Any, Dict, List, Optional

def render_soniox_tokens(tokens: List[Dict[str, Any]]) -> str:
    """
    Render a list of Soniox tokens to a readable transcript string.

    Mirrors the behaviour of the official Soniox SDK's `renderTokens` helper:
    - When the speaker changes, a `Speaker N:` tag is inserted.
    - When the language changes, a `[lang]` (or `[Translation][lang]`) tag is
      inserted.

    If neither speaker nor language information is present on any token (i.e.
    diarization and language identification are disabled), the function simply
    concatenates the token texts.
    """
    if not tokens:
        return ""

    text_parts: List[str] = []
    current_speaker: Optional[Any] = None
    current_language: Optional[Any] = None

    for token in tokens:
        text = token.get("text", "")
        speaker = token.get("speaker")
        language = token.get("language")
        is_translation = token.get("translation_status") == "translation"

        # Speaker changed -> emit a speaker tag.
        if speaker is not None and speaker != current_speaker:
            if current_speaker is not None:
                text_parts.append("\n\n")
            current_speaker = speaker
            current_language = None  # reset language whenever speaker changes
            text_parts.append(f"Speaker {current_speaker}:")

        # Language changed -> emit a language (or translation) tag.
        if language is not None and language != current_language:
            current_language = language
            prefix = "[Translation] " if is_translation else ""
            text_parts.append(f"\n{prefix}[{current_language}] ")
            text = text.lstrip() if isinstance(text, str) else text

        text_parts.append(text)

    return "".join(text_parts)

