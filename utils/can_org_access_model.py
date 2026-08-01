
def can_org_access_model(
    model: str,
    org_object: Optional[LiteLLM_OrganizationTable],
    llm_router: Optional[Router],
    team_model_aliases: Optional[Dict[str, str]] = None,
) -> Literal[True]:
    """
    Returns True if the team can access a specific model.

    """
    return _can_object_call_model(
        model=model,
        llm_router=llm_router,
        models=org_object.models if org_object else [],
        team_model_aliases=team_model_aliases,
        object_type="org",
    )

