
def _call_llm(
    prompt: str,
    model_name: str,
    litellm_kwargs: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    """Call the LLM (streaming) and return ``(response_text, call_details)``.

    The response is streamed via ``stream=True`` and assembled before return,
    so callers see the same blocking-style ``(text, details)`` interface.

    ``call_details`` contains per-call usage and metadata::

        {
            "prompt_tokens": int | None,
            "generation_tokens": int | None,
            "reasoning_tokens": int | None,
            "total_tokens": int | None,
            "finish_reason": str | None,
            "duration_secs": float,
            "first_token_secs": float,  # only when any content streamed
        }
    """
    _TELEMETRY(calling_llm=True)
    start = time.perf_counter()
    first_token_secs: float | None = None
    try:
        # Per-LLM-call timeout. Honors LLM_CALL_TIMEOUT env var so the
        # ablation runner (or any orchestrator) can dial it without
        # changing the harness contract. Default 3600s preserves the
        # historical behavior.
        call_timeout = int(os.environ.get("LLM_CALL_TIMEOUT", "3600"))
        stream = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            timeout=call_timeout,
            stream=True,
            stream_options={"include_usage": True},
            **litellm_kwargs,
        )

        content_parts: list[str] = []
        finish_reason: str | None = None
        usage_obj: Any = None
        for chunk in stream:
            choices = getattr(chunk, "choices", None) or []
            if choices:
                delta = getattr(choices[0], "delta", None)
                piece = getattr(delta, "content", None) if delta else None
                if piece:
                    if first_token_secs is None:
                        first_token_secs = time.perf_counter() - start
                    content_parts.append(piece)
                fr = getattr(choices[0], "finish_reason", None)
                if fr:
                    finish_reason = fr
            chunk_usage = getattr(chunk, "usage", None)
            if chunk_usage is not None:
                usage_obj = chunk_usage

        content = "".join(content_parts).strip()
        duration = time.perf_counter() - start

        if not content:
            raise RuntimeError(
                "LLM stream produced no content "
                f"(finish_reason={finish_reason!r}, duration_secs={duration:.3f})"
            )
        if finish_reason is None:
            raise RuntimeError(
                "LLM stream ended without a finish_reason "
                f"(content_length={len(content)}, duration_secs={duration:.3f})"
            )

        ctd = (
            getattr(usage_obj, "completion_tokens_details", None)
            if usage_obj
            else None
        )
        reasoning_tokens = (
            getattr(ctd, "reasoning_tokens", None) if ctd else None
        )

        details: dict[str, Any] = {
            "prompt_tokens": getattr(usage_obj, "prompt_tokens", None),
            "generation_tokens": getattr(
                usage_obj, "completion_tokens", None,
            ),
            "total_tokens": getattr(usage_obj, "total_tokens", None),
            "finish_reason": finish_reason,
            "duration_secs": round(duration, 3),
        }
        if reasoning_tokens is not None:
            details["reasoning_tokens"] = reasoning_tokens
        if first_token_secs is not None:
            details["first_token_secs"] = round(first_token_secs, 3)
        _TELEMETRY(
            llm_call_success=True,
            duration_secs=details["duration_secs"],
            prompt_tokens=details["prompt_tokens"],
            completion_tokens=details["generation_tokens"],
        )
        return content, details
    except Exception as exc:
        duration = time.perf_counter() - start
        _TELEMETRY(
            llm_call_exception=str(exc),
            duration_secs=round(duration, 3),
        )
        raise

