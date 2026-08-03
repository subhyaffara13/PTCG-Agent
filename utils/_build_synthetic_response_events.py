from typing import Any, List, Optional

def _build_synthetic_response_events(
    *,
    transformed: Any,
    logging_obj: LiteLLMLoggingObj,
    chunk_size: int,
) -> List[Any]:
    openai_types = _get_openai_response_types()
    if litellm.include_cost_in_streaming_usage and logging_obj is not None:
        usage_obj: Optional[Any] = getattr(transformed, "usage", None)
        if usage_obj is not None:
            try:
                cost: Optional[float] = logging_obj._response_cost_calculator(
                    result=transformed
                )
                if cost is not None:
                    setattr(usage_obj, "cost", cost)
            except Exception:
                pass

    events: List[Any] = [
        _build_response_status_event(
            openai_types.ResponsesAPIStreamEvents.RESPONSE_CREATED, transformed
        ),
        _build_response_status_event(
            openai_types.ResponsesAPIStreamEvents.RESPONSE_IN_PROGRESS, transformed
        ),
    ]

    sequence_number = 0
    for output_index, output_item in enumerate(
        getattr(transformed, "output", []) or []
    ):
        output_item_payload = _dump_response_object(output_item)
        item_id = str(output_item_payload.get("id") or transformed.id)
        item_type = output_item_payload.get("type")

        events.append(
            openai_types.OutputItemAddedEvent(
                type=openai_types.ResponsesAPIStreamEvents.OUTPUT_ITEM_ADDED,
                output_index=output_index,
                item=openai_types.BaseLiteLLMOpenAIResponseObject(
                    **output_item_payload
                ),
            )
        )

        if item_type == "message":
            for content_index, part in enumerate(
                output_item_payload.get("content", []) or []
            ):
                part_payload = _dump_response_object(part)
                events.append(
                    openai_types.ContentPartAddedEvent(
                        type=openai_types.ResponsesAPIStreamEvents.CONTENT_PART_ADDED,
                        item_id=item_id,
                        output_index=output_index,
                        content_index=content_index,
                        part=openai_types.BaseLiteLLMOpenAIResponseObject(
                            **part_payload
                        ),
                    )
                )
                _add_text_like_part_events(
                    events=events,
                    item_id=item_id,
                    output_index=output_index,
                    content_index=content_index,
                    part_payload=part_payload,
                    chunk_size=chunk_size,
                )
                done_event = _build_content_part_done_event(
                    item_id=item_id,
                    output_index=output_index,
                    content_index=content_index,
                    part_payload=part_payload,
                )
                if done_event is not None:
                    events.append(done_event)
        elif item_type == "function_call":
            arguments = str(output_item_payload.get("arguments") or "")
            for i in range(0, len(arguments), chunk_size):
                events.append(
                    openai_types.FunctionCallArgumentsDeltaEvent(
                        type=openai_types.ResponsesAPIStreamEvents.FUNCTION_CALL_ARGUMENTS_DELTA,
                        item_id=item_id,
                        output_index=output_index,
                        delta=arguments[i : i + chunk_size],
                    )
                )
            events.append(
                openai_types.FunctionCallArgumentsDoneEvent(
                    type=openai_types.ResponsesAPIStreamEvents.FUNCTION_CALL_ARGUMENTS_DONE,
                    item_id=item_id,
                    output_index=output_index,
                    arguments=arguments,
                )
            )
        elif item_type == "reasoning":
            for summary_index, summary in enumerate(
                output_item_payload.get("summary", []) or []
            ):
                summary_payload = _dump_response_object(summary)
                summary_text = str(summary_payload.get("text") or "")
                for i in range(0, len(summary_text), chunk_size):
                    events.append(
                        openai_types.ReasoningSummaryTextDeltaEvent(
                            type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_TEXT_DELTA,
                            item_id=item_id,
                            output_index=output_index,
                            summary_index=summary_index,
                            delta=summary_text[i : i + chunk_size],
                        )
                    )
                sequence_number += 1
                events.append(
                    openai_types.ReasoningSummaryTextDoneEvent(
                        type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_TEXT_DONE,
                        item_id=item_id,
                        output_index=output_index,
                        sequence_number=sequence_number,
                        summary_index=summary_index,
                        text=summary_text,
                    )
                )
                sequence_number += 1
                events.append(
                    openai_types.ReasoningSummaryPartDoneEvent(
                        type=openai_types.ResponsesAPIStreamEvents.REASONING_SUMMARY_PART_DONE,
                        item_id=item_id,
                        output_index=output_index,
                        sequence_number=sequence_number,
                        summary_index=summary_index,
                        part=openai_types.BaseLiteLLMOpenAIResponseObject(
                            **summary_payload
                        ),
                    )
                )

        sequence_number += 1
        events.append(
            openai_types.OutputItemDoneEvent(
                type=openai_types.ResponsesAPIStreamEvents.OUTPUT_ITEM_DONE,
                output_index=output_index,
                sequence_number=sequence_number,
                item=openai_types.BaseLiteLLMOpenAIResponseObject(
                    **output_item_payload
                ),
            )
        )

    events.append(
        openai_types.ResponseCompletedEvent(
            type=openai_types.ResponsesAPIStreamEvents.RESPONSE_COMPLETED,
            response=transformed,
        )
    )
    return events

