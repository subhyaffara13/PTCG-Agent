
def _record_to_response(record) -> AccessGroupResponse:
    return AccessGroupResponse(
        access_group_id=record.access_group_id,
        access_group_name=record.access_group_name,
        description=record.description,
        access_model_names=record.access_model_names,
        access_mcp_server_ids=record.access_mcp_server_ids,
        access_agent_ids=record.access_agent_ids,
        assigned_team_ids=record.assigned_team_ids,
        assigned_key_ids=record.assigned_key_ids,
        created_at=record.created_at,
        created_by=record.created_by,
        updated_at=record.updated_at,
        updated_by=record.updated_by,
    )

