
def _add_text_like_part_events(
    *,
    events: List[Any],
    item_id: str,
    output_index: int,
    content_index: int,
    part_payload: Dict[str, Any],
    chunk_size: int,
) -> None:
    openai_types = _get_openai_response_types()
    part_type = part_payload.get("type")
    if part_type == "output_text":
        text = str(part_payload.get("text") or "")
        for i in range(0, len(text), chunk_size):
            events.append(
                openai_types.OutputTextDeltaEvent(
                    type=openai_types.ResponsesAPIStreamEvents.OUTPUT_TEXT_DELTA,
                    item_id=item_id,
                    output_index=output_index,
                    content_index=content_index,
                    delta=text[i : i + chunk_size],
                )
            )
        for annotation_index, annotation in enumerate(
            part_payload.get("annotations", []) or []
        ):
            events.append(
                openai_types.OutputTextAnnotationAddedEvent(
                    type=openai_types.ResponsesAPIStreamEvents.OUTPUT_TEXT_ANNOTATION_ADDED,
                    item_id=item_id,
                    output_index=output_index,
                    content_index=content_index,
                    annotation_index=annotation_index,
                    annotation=annotation,
                )
            )
        events.append(
            openai_types.OutputTextDoneEvent(
                type=openai_types.ResponsesAPIStreamEvents.OUTPUT_TEXT_DONE,
                item_id=item_id,
                output_index=output_index,
                content_index=content_index,
                text=text,
            )
        )
    elif part_type == "refusal":
        refusal = str(part_payload.get("refusal") or "")
        for i in range(0, len(refusal), chunk_size):
            events.append(
                openai_types.RefusalDeltaEvent(
                    type=openai_types.ResponsesAPIStreamEvents.REFUSAL_DELTA,
                    item_id=item_id,
                    output_index=output_index,
                    content_index=content_index,
                    delta=refusal[i : i + chunk_size],
                )
            )
        events.append(
            openai_types.RefusalDoneEvent(
                type=openai_types.ResponsesAPIStreamEvents.REFUSAL_DONE,
                item_id=item_id,
                output_index=output_index,
                content_index=content_index,
                refusal=refusal,
            )
        )

