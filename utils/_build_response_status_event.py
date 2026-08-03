from typing import Any

def _build_response_status_event(
    event_type: Literal[
        "response.created",
        "response.in_progress",
    ],
    transformed: Any,
) -> Any:
    openai_types = _get_openai_response_types()
    in_progress_response = transformed.model_copy(
        deep=True,
        update={"status": "in_progress", "output": []},
    )
    if event_type == openai_types.ResponsesAPIStreamEvents.RESPONSE_CREATED:
        return openai_types.ResponseCreatedEvent(
            type=event_type, response=in_progress_response
        )
    return openai_types.ResponseInProgressEvent(
        type=event_type, response=in_progress_response
    )

