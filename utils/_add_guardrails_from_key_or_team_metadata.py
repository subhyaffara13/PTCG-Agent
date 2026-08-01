
def _add_guardrails_from_key_or_team_metadata(
    key_metadata: Optional[dict],
    team_metadata: Optional[dict],
    data: dict,
    metadata_variable_name: str,
    project_metadata: Optional[dict] = None,
) -> None:
    """
    Helper add guardrails from key, team, or project metadata to request data

    Key guardrails are set first, then team and project guardrails are appended (without duplicates).

    Args:
        key_metadata: The key metadata dictionary to check for guardrails
        team_metadata: The team metadata dictionary to check for guardrails
        data: The request data to update
        metadata_variable_name: The name of the metadata field in data
        project_metadata: The project metadata dictionary to check for guardrails

    """
    from litellm.proxy.utils import _premium_user_check

    # Initialize guardrails set (avoiding duplicates)
    combined_guardrails = set()

    # Add key-level guardrails first
    if key_metadata and "guardrails" in key_metadata:
        if (
            isinstance(key_metadata["guardrails"], list)
            and len(key_metadata["guardrails"]) > 0
        ):
            _premium_user_check()
            combined_guardrails.update(key_metadata["guardrails"])

    # Add team-level guardrails (set automatically handles duplicates)
    if team_metadata and "guardrails" in team_metadata:
        if (
            isinstance(team_metadata["guardrails"], list)
            and len(team_metadata["guardrails"]) > 0
        ):
            _premium_user_check()
            combined_guardrails.update(team_metadata["guardrails"])

    # Add project-level guardrails (set automatically handles duplicates)
    if project_metadata and "guardrails" in project_metadata:
        if (
            isinstance(project_metadata["guardrails"], list)
            and len(project_metadata["guardrails"]) > 0
        ):
            _premium_user_check()
            combined_guardrails.update(project_metadata["guardrails"])

    # Set combined guardrails in metadata as list
    if combined_guardrails:
        data[metadata_variable_name]["guardrails"] = list(combined_guardrails)

