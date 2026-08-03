from typing import Any, Dict, List, Optional

def build_trace_payload(
    project_name: str,
    trace_id: str,
    response_obj: Dict[str, Any],
    start_time: datetime,
    end_time: datetime,
    input_data: Any,
    output_data: Any,
    metadata: Dict[str, Any],
    tags: List[str],
    thread_id: Optional[str],
) -> types.TracePayload:
    """Build a complete trace payload."""
    trace_name = response_obj.get("object", "unknown type")

    return types.TracePayload(
        project_name=project_name,
        id=trace_id,
        name=trace_name,
        start_time=(
            start_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        ),
        end_time=end_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        input=input_data,
        output=output_data,
        metadata=metadata,
        tags=tags,
        thread_id=thread_id,
    )

