
def _extract_scim_user_data(user: SCIMUser) -> ScimUserData:
    """Extract common data from SCIMUser object."""
    user_email = None
    if user.emails and len(user.emails) > 0:
        user_email = user.emails[0].value

    user_alias = None
    if user.name and user.name.givenName:
        user_alias = user.name.givenName

    teams = []
    if user.groups:
        teams = [group.value for group in user.groups]

    return {
        "user_email": user_email,
        "user_alias": user_alias,
        "sso_user_id": user.externalId,
        "teams": teams,
        "given_name": user.name.givenName if user.name else None,
        "family_name": user.name.familyName if user.name else None,
        "active": user.active,
    }

