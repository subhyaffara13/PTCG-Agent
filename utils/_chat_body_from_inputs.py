from typing import List

def _chat_body_from_inputs(
    inputs: GenericGuardrailAPIInputs, agent_id: str, request_data: dict
) -> dict:
    """Build a chat completion request body from guardrail inputs and agent_id."""
    messages: List[dict]
    structured = inputs.get("structured_messages")
    texts = inputs.get("texts")
    if structured:
        messages = list(structured)  # type: ignore[arg-type]
    elif texts:
        if len(texts) == 1:
            messages = [{"role": "user", "content": texts[0]}]
        else:
            messages = [{"role": "user", "content": "\n".join(texts)}]
    else:
        messages = [{"role": "user", "content": "Hello"}]
    body: dict = {"model": agent_id, "messages": messages, "stream": False}
    if request_data:
        body.setdefault("metadata", {}).update(request_data)
    return body

