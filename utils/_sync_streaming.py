
def _sync_streaming(
    response: httpx.Response,
    litellm_logging_obj: "LiteLLMLoggingObj",
    provider_config: "BasePassthroughConfig",
):
    from litellm.utils import executor

    raw_bytes: List[bytes] = []
    flush_scheduled = False
    try:
        for chunk in response.iter_bytes():  # type: ignore
            raw_bytes.append(chunk)
            yield chunk
    finally:
        if not flush_scheduled and raw_bytes:
            flush_scheduled = True
            try:
                executor.submit(
                    litellm_logging_obj.flush_passthrough_collected_chunks,
                    raw_bytes=raw_bytes,
                    provider_config=provider_config,
                )
            except Exception as e:
                verbose_logger.exception(
                    "Failed to schedule passthrough spend-tracking flush "
                    "in _sync_streaming; %d buffered chunks dropped: %s",
                    len(raw_bytes),
                    e,
                )

