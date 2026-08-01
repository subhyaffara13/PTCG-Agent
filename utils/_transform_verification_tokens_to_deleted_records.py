
def _transform_verification_tokens_to_deleted_records(
    keys: List[LiteLLM_VerificationToken],
    user_api_key_dict: UserAPIKeyAuth,
    litellm_changed_by: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Transform verification tokens into deleted token records ready for persistence."""
    if not keys:
        return []

    deleted_at = datetime.now(timezone.utc)
    records = []
    for key in keys:
        key_payload = key.model_dump()
        deleted_record = LiteLLM_DeletedVerificationToken(
            **key_payload,
            deleted_at=deleted_at,
            deleted_by=user_api_key_dict.user_id,
            deleted_by_api_key=user_api_key_dict.api_key,
            litellm_changed_by=litellm_changed_by,
        )
        record = deleted_record.model_dump()

        # Map org_id to organization_id (model uses org_id, but schema expects organization_id)
        org_id_value = record.pop("org_id", None)
        if org_id_value is not None:
            record["organization_id"] = org_id_value

        for json_field in [
            "aliases",
            "config",
            "permissions",
            "metadata",
            "model_spend",
            "model_max_budget",
            "router_settings",
        ]:
            if json_field in record and record[json_field] is not None:
                record[json_field] = json.dumps(record[json_field])

        for rel_key in (
            "litellm_budget_table",
            "litellm_organization_table",
            "object_permission",
            "id",
            "budget_limits",
        ):
            record.pop(rel_key, None)

        records.append(record)

    return records

