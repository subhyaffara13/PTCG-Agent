
def llm_call_span_name(data: "LLMCallSpanData") -> str:
    """``"{operation} {model}"`` e.g. ``"chat gpt-4o"`` (GenAI semconv)."""
    model = data.request_model or ""
    return f"{data.operation.value} {model}".strip()

