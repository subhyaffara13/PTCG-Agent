from typing import Any, Dict, Optional

def _build_content_part_done_event(
    *,
    item_id: str,
    output_index: int,
    content_index: int,
    part_payload: Dict[str, Any],
) -> Optional[Any]:
    openai_types = _get_openai_response_types()
    part_type = part_payload.get("type")
    part: Any
    if part_type == "output_text":
        annotations = [
            openai_types.BaseLiteLLMOpenAIResponseObject(**annotation)
            for annotation in part_payload.get("annotations", []) or []
        ]
        part = openai_types.ContentPartDonePartOutputText(
            type="output_text",
            text=str(part_payload.get("text") or ""),
            annotations=annotations,
            logprobs=part_payload.get("logprobs"),
        )
    elif part_type == "refusal":
        part = openai_types.ContentPartDonePartRefusal(
            type="refusal",
            refusal=str(part_payload.get("refusal") or ""),
        )
    elif part_type == "reasoning_text":
        part = openai_types.ContentPartDonePartReasoningText(
            type="reasoning_text",
            reasoning=str(part_payload.get("reasoning") or ""),
        )
    else:
        return None

    return openai_types.ContentPartDoneEvent(
        type=openai_types.ResponsesAPIStreamEvents.CONTENT_PART_DONE,
        item_id=item_id,
        output_index=output_index,
        content_index=content_index,
        part=part,
    )

