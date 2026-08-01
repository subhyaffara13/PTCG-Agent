
def can_modify_guardrails(team_obj: Optional[LiteLLM_TeamTable]) -> bool:
    if team_obj is None:
        return True

    team_metadata = team_obj.metadata or {}

    if team_metadata.get("guardrails", None) is not None and isinstance(
        team_metadata.get("guardrails"), Dict
    ):
        if team_metadata.get("guardrails", {}).get("modify_guardrails", None) is False:
            return False

    return True

