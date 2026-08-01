
def _build_audit_log_payload(
    request_data: LiteLLM_AuditLogs,
) -> StandardAuditLogPayload:
    """Convert LiteLLM_AuditLogs to StandardAuditLogPayload for callback dispatch."""
    updated_at = ""
    if request_data.updated_at is not None:
        updated_at = request_data.updated_at.isoformat()

    table_name_str: str = (
        request_data.table_name.value
        if isinstance(request_data.table_name, LitellmTableNames)
        else str(request_data.table_name)
    )

    return StandardAuditLogPayload(
        id=request_data.id,
        updated_at=updated_at,
        changed_by=request_data.changed_by or "",
        changed_by_api_key=request_data.changed_by_api_key or "",
        action=request_data.action,
        table_name=table_name_str,
        object_id=request_data.object_id,
        before_value=request_data.before_value,
        updated_values=request_data.updated_values,
    )

