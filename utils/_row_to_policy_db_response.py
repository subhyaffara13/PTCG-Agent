from typing import Any

def _row_to_policy_db_response(row: Any) -> PolicyDBResponse:
    """Build PolicyDBResponse from a Prisma LiteLLM_PolicyTable row."""
    return PolicyDBResponse(
        policy_id=row.policy_id,
        policy_name=row.policy_name,
        version_number=getattr(row, "version_number", 1),
        version_status=getattr(row, "version_status", "production"),
        parent_version_id=getattr(row, "parent_version_id", None),
        is_latest=getattr(row, "is_latest", True),
        published_at=getattr(row, "published_at", None),
        production_at=getattr(row, "production_at", None),
        inherit=row.inherit,
        description=row.description,
        guardrails_add=row.guardrails_add or [],
        guardrails_remove=row.guardrails_remove or [],
        condition=row.condition,
        pipeline=row.pipeline,
        created_at=row.created_at,
        updated_at=row.updated_at,
        created_by=row.created_by,
        updated_by=row.updated_by,
    )

