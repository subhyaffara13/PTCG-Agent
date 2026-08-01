
def _parse_prompt_tokens_details(usage: Usage) -> PromptTokensDetailsResult:
    cache_hit_tokens = (
        cast(Optional[int], getattr(usage.prompt_tokens_details, "cached_tokens", 0))
        or 0
    )
    cache_creation_tokens = (
        cast(
            Optional[int],
            getattr(usage.prompt_tokens_details, "cache_creation_tokens", 0),
        )
        or 0
    )
    cache_creation_token_details = (
        cast(
            Optional[CacheCreationTokenDetails],
            getattr(usage.prompt_tokens_details, "cache_creation_token_details", None),
        )
        or None
    )
    text_tokens = (
        cast(Optional[int], getattr(usage.prompt_tokens_details, "text_tokens", None))
        or 0  # default to prompt tokens, if this field is not set
    )
    audio_tokens = (
        cast(Optional[int], getattr(usage.prompt_tokens_details, "audio_tokens", 0))
        or 0
    )
    image_tokens = (
        cast(Optional[int], getattr(usage.prompt_tokens_details, "image_tokens", 0))
        or 0
    )
    character_count = (
        cast(
            Optional[int],
            getattr(usage.prompt_tokens_details, "character_count", 0),
        )
        or 0
    )
    image_count = (
        cast(Optional[int], getattr(usage.prompt_tokens_details, "image_count", 0)) or 0
    )
    video_length_seconds = (
        cast(
            Optional[float],
            getattr(usage.prompt_tokens_details, "video_length_seconds", 0),
        )
        or 0.0
    )

    return PromptTokensDetailsResult(
        cache_hit_tokens=cache_hit_tokens,
        cache_creation_tokens=cache_creation_tokens,
        cache_creation_token_details=cache_creation_token_details,
        text_tokens=text_tokens,
        audio_tokens=audio_tokens,
        image_tokens=image_tokens,
        character_count=character_count,
        image_count=image_count,
        video_length_seconds=float(video_length_seconds),
    )

