
def _infer_open_inference_span_kind(call_type: Optional[str]) -> str:
    """
    Map LiteLLM call types to OpenInference span kinds.
    """

    if not call_type:
        return OpenInferenceSpanKindValues.UNKNOWN.value

    lowered = str(call_type).lower()

    if "embed" in lowered:
        return OpenInferenceSpanKindValues.EMBEDDING.value

    if "rerank" in lowered:
        return OpenInferenceSpanKindValues.RERANKER.value

    if "search" in lowered:
        return OpenInferenceSpanKindValues.RETRIEVER.value

    if "moderation" in lowered or "guardrail" in lowered:
        return OpenInferenceSpanKindValues.GUARDRAIL.value

    if lowered == "call_mcp_tool" or lowered == "mcp" or lowered.endswith("tool"):
        return OpenInferenceSpanKindValues.TOOL.value

    if "asend_message" in lowered or "a2a" in lowered or "assistant" in lowered:
        return OpenInferenceSpanKindValues.AGENT.value

    if any(
        keyword in lowered
        for keyword in (
            "completion",
            "chat",
            "image",
            "audio",
            "speech",
            "transcription",
            "generate_content",
            "response",
            "videos",
            "realtime",
            "pass_through",
            # `passthrough` (no underscore) is what real call_types use:
            # `allm_passthrough_route`, `llm_passthrough_route`. Without
            # this they fell through to UNKNOWN, blanking span.kind.
            "passthrough",
            "anthropic_messages",
            "ocr",
        )
    ):
        return OpenInferenceSpanKindValues.LLM.value

    if any(
        keyword in lowered
        for keyword in ("file", "batch", "container", "fine_tuning_job")
    ):
        return OpenInferenceSpanKindValues.CHAIN.value

    return OpenInferenceSpanKindValues.UNKNOWN.value

