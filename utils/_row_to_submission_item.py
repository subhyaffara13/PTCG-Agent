from typing import Any

def _row_to_submission_item(row: Any) -> GuardrailSubmissionItem:
    from litellm.litellm_core_utils.litellm_logging import _get_masked_values

    guardrail_info = _parse_json_field(row.guardrail_info) or {}
    team_guardrail = row.team_id is not None
    raw_params = _parse_json_field(row.litellm_params) or {}
    masked_params = _get_masked_values(
        raw_params, unmasked_length=4, number_of_asterisks=4
    )
    return GuardrailSubmissionItem(
        guardrail_id=row.guardrail_id,
        guardrail_name=row.guardrail_name,
        status=row.status or "active",
        team_id=row.team_id,
        team_guardrail=team_guardrail,
        litellm_params=masked_params,
        guardrail_info=guardrail_info,
        submitted_by_user_id=guardrail_info.get("submitted_by_user_id"),
        submitted_by_email=guardrail_info.get("submitted_by_email"),
        submitted_at=getattr(row, "submitted_at", None),
        reviewed_at=getattr(row, "reviewed_at", None),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )

