import json
from typing import Any, Dict, List, Optional

def _transform_teams_to_deleted_records(
    teams: List[LiteLLM_TeamTable],
    user_api_key_dict: UserAPIKeyAuth,
    litellm_changed_by: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Transform teams into deleted team records ready for persistence."""
    if not teams:
        return []

    deleted_at = datetime.now(timezone.utc)
    records = []
    for team in teams:
        team_payload = team.model_dump()
        deleted_record = LiteLLM_DeletedTeamTable(
            **team_payload,
            deleted_at=deleted_at,
            deleted_by=user_api_key_dict.user_id,
            deleted_by_api_key=user_api_key_dict.api_key,
            litellm_changed_by=litellm_changed_by,
        )
        record = deleted_record.model_dump()

        for json_field in [
            "members_with_roles",
            "metadata",
            "model_spend",
            "model_max_budget",
            "router_settings",
        ]:
            if json_field in record and record[json_field] is not None:
                record[json_field] = json.dumps(record[json_field])

        for rel_key in (
            "litellm_model_table",
            "object_permission",
            "id",
            "budget_limits",  # not in LiteLLM_DeletedTeamTable schema
            "default_team_member_models",  # not in LiteLLM_DeletedTeamTable schema
        ):
            record.pop(rel_key, None)

        records.append(record)

    return records

