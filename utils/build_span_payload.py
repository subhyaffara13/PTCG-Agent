
def build_span_payload(
    project_name: str,
    trace_id: str,
    parent_span_id: Optional[str],
    response_obj: Dict[str, Any],
    start_time: datetime,
    end_time: datetime,
    input_data: Any,
    output_data: Any,
    metadata: Dict[str, Any],
    tags: List[str],
    usage: Dict[str, int],
    provider: Optional[str] = None,
    cost: Optional[float] = None,
) -> types.SpanPayload:
    """Build a complete span payload."""
    span_id = utils.create_uuid7()

    model = response_obj.get("model", "unknown-model")
    obj_type = response_obj.get("object", "unknown-object")
    created = response_obj.get("created", 0)
    span_name = f"{model}_{obj_type}_{created}"

    _logging.verbose_logger.debug(
        f"OpikLogger creating span with id {span_id} for trace {trace_id}"
    )

    return types.SpanPayload(
        id=span_id,
        project_name=project_name,
        trace_id=trace_id,
        parent_span_id=parent_span_id,
        name=span_name,
        type="llm",
        model=model,
        start_time=(
            start_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        ),
        end_time=end_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        input=input_data,
        output=output_data,
        metadata=metadata,
        tags=tags,
        usage=usage,
        provider=provider,
        total_cost=cost,
    )

