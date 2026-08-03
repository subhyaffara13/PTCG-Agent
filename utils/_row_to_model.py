from typing import Any, Union

def _row_to_model(row: Union[dict, Any]) -> LiteLLM_ToolTableRow:
    """Convert a Prisma model instance or dict to LiteLLM_ToolTableRow."""
    model_dump = getattr(row, "model_dump", None)
    if callable(model_dump):
        row = model_dump()
    elif not isinstance(row, dict):
        row = {
            k: getattr(row, k, None)
            for k in (
                "tool_id",
                "tool_name",
                "origin",
                "input_policy",
                "output_policy",
                "call_count",
                "assignments",
                "key_hash",
                "team_id",
                "key_alias",
                "user_agent",
                "last_used_at",
                "created_at",
                "updated_at",
                "created_by",
                "updated_by",
            )
        }
    return LiteLLM_ToolTableRow(
        tool_id=row.get("tool_id", ""),
        tool_name=row.get("tool_name", ""),
        origin=row.get("origin"),
        input_policy=row.get("input_policy") or "untrusted",
        output_policy=row.get("output_policy") or "untrusted",
        call_count=int(row.get("call_count") or 0),
        assignments=row.get("assignments"),
        key_hash=row.get("key_hash"),
        team_id=row.get("team_id"),
        key_alias=row.get("key_alias"),
        user_agent=row.get("user_agent"),
        last_used_at=row.get("last_used_at"),
        created_at=row.get("created_at"),
        updated_at=row.get("updated_at"),
        created_by=row.get("created_by"),
        updated_by=row.get("updated_by"),
    )


def _row_to_model(row: Any) -> LiteLLM_MemoryRow:
    return LiteLLM_MemoryRow(
        memory_id=row.memory_id,
        key=row.key,
        value=row.value,
        metadata=getattr(row, "metadata", None),
        user_id=row.user_id,
        team_id=row.team_id,
        created_at=row.created_at,
        created_by=row.created_by,
        updated_at=row.updated_at,
        updated_by=row.updated_by,
    )

