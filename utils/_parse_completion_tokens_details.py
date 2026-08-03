from typing import Optional

def _parse_completion_tokens_details(usage: Usage) -> CompletionTokensDetailsResult:
    audio_tokens = (
        cast(
            Optional[int],
            getattr(usage.completion_tokens_details, "audio_tokens", 0),
        )
        or 0
    )
    text_tokens = (
        cast(
            Optional[int],
            getattr(usage.completion_tokens_details, "text_tokens", None),
        )
        or 0  # default to completion tokens, if this field is not set
    )
    reasoning_tokens = (
        cast(
            Optional[int],
            getattr(usage.completion_tokens_details, "reasoning_tokens", 0),
        )
        or 0
    )
    image_tokens = (
        cast(
            Optional[int],
            getattr(usage.completion_tokens_details, "image_tokens", 0),
        )
        or 0
    )

    return CompletionTokensDetailsResult(
        audio_tokens=audio_tokens,
        text_tokens=text_tokens,
        reasoning_tokens=reasoning_tokens,
        image_tokens=image_tokens,
    )

