
def get_resource_owner_scopes(
    user_api_key_dict: Optional[UserAPIKeyAuth],
) -> List[str]:
    """
    Return ownership scopes that may access a user-created proxy resource.

    Raw user_id is included for rows created before scope prefixes existed.
    Prefixes avoid collisions when falling back to team/org/key ownership
    for keys that do not have a user_id.

    Identity-less callers (no user_id, team_id, org_id, api_key, or token)
    return ``[]`` — they share no scope with any other caller, so access
    checks against an existing owner always fail and creates that depend
    on a primary scope must reject up front. Returning a shared sentinel
    here would let any two identity-less callers see each other's data.
    """
    if user_api_key_dict is None:
        return []

    scopes: List[str] = []

    def _add(scope: Optional[str]) -> None:
        if scope and scope not in scopes:
            scopes.append(scope)

    if user_api_key_dict.user_id:
        _add(user_api_key_dict.user_id)
        _add(f"user:{user_api_key_dict.user_id}")
    if user_api_key_dict.team_id:
        _add(f"team:{user_api_key_dict.team_id}")
    if user_api_key_dict.org_id:
        _add(f"org:{user_api_key_dict.org_id}")
    if user_api_key_dict.api_key:
        _add(f"key:{user_api_key_dict.api_key}")
    if user_api_key_dict.token:
        _add(f"key:{user_api_key_dict.token}")

    return scopes

