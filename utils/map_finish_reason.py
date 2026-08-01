
def map_finish_reason(finish_reason: str) -> OpenAIChatCompletionFinishReason:
    mapped = _FINISH_REASON_MAP.get(finish_reason)
    if mapped is None:
        verbose_logger.warning(
            "Unmapped finish_reason '%s', defaulting to 'stop'", finish_reason
        )
        return "stop"
    return mapped

