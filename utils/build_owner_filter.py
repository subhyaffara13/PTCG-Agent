
def build_owner_filter(
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Dict[str, Any]]:
    """Return a Prisma `where` fragment that scopes a managed-resource listing
    to records the caller is allowed to see.

    - ``{}`` means no scoping (proxy admins).
    - ``{"created_by": <user_id>}`` for user-keyed callers.
    - ``{"team_id": <team_id>}`` for service-account callers
      that have a team but no user_id.
    - ``{"OR": [...]}`` when the caller has both — listing must include
      both their own resources and team-shared ones so it stays consistent
      with ``can_access_resource``.
    - ``None`` means deny: callers MUST skip the query rather than fall
      back to an unscoped fetch.
    """
    if _user_has_admin_view(user_api_key_dict):
        return {}

    user_id = user_api_key_dict.user_id
    team_id = user_api_key_dict.team_id

    if user_id is not None and team_id is not None:
        return {
            "OR": [
                {"created_by": user_id},
                {"team_id": team_id},
            ]
        }

    if user_id is not None:
        return {"created_by": user_id}

    if team_id is not None:
        return {"team_id": team_id}

    return None

