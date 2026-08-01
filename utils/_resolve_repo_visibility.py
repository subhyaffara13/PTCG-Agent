
def _resolve_repo_visibility(
    *,
    private: bool | None,
    visibility: RepoVisibility_T | None,
    repo_type: str | None,
) -> RepoVisibility_T | None:
    if private is not None and visibility is not None:
        raise ValueError("Received both `private` and `visibility` arguments. Please provide only one of them.")

    if visibility is None:
        if private is None:
            return None
        return "private" if private else "public"

    if visibility == "protected" and repo_type != constants.REPO_TYPE_SPACE:
        raise ValueError("Only Spaces can be 'protected'. Please set visibility to 'public' or 'private'.")
    return visibility

