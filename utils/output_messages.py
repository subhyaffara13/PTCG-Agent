
def output_messages(data: LLMCallSpanData) -> list:
    """The ``message`` payload of each response choice."""
    return [c.get("message") for c in data.choices_out if isinstance(c, dict)]

