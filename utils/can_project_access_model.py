
def can_project_access_model(
    model: Union[str, List[str]],
    project_object: LiteLLM_ProjectTableCachedObj,
    llm_router: Optional[Router],
) -> Literal[True]:
    """
    Returns True if the project can access a specific model.

    Raises ProxyException if access is denied.
    """
    return _can_object_call_model(
        model=model,
        llm_router=llm_router,
        models=project_object.models if project_object else [],
        object_type="project",
    )

