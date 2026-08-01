
def can_access_resource(
    user_api_key_dict: UserAPIKeyAuth,
    created_by: Optional[str],
    resource_team_id: Optional[str],
) -> bool:
    """Return True iff the caller may read/modify a managed resource.

    The resource's ``created_by`` and ``team_id`` fields must be non-None
    to match the caller's identity — guarding against the ``None == None``
    bypass that previously let service-account keys read every keyless
    resource.
    """
    if _user_has_admin_view(user_api_key_dict):
        return True

    user_id = user_api_key_dict.user_id
    if user_id is not None and created_by is not None and created_by == user_id:
        return True

    team_id = user_api_key_dict.team_id
    if (
        team_id is not None
        and resource_team_id is not None
        and resource_team_id == team_id
    ):
        return True

    return False

