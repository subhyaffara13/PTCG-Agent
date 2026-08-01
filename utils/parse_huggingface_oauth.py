
def parse_huggingface_oauth(request: "fastapi.Request") -> OAuthInfo | None:
    """
    Returns the information from a logged-in user as a [`OAuthInfo`] object.

    For flexibility and future-proofing, this method is very lax in its parsing and does not raise errors.
    Missing fields are set to `None` without a warning.

    Return `None`, if the user is not logged in (no info in session cookie).

    See [`attach_huggingface_oauth`] for an example on how to use this method.
    """
    if "oauth_info" not in request.session:
        logger.debug("No OAuth info in session.")
        return None

    logger.debug("Parsing OAuth info from session.")
    oauth_data = request.session["oauth_info"]
    user_data = oauth_data.get("userinfo", {})
    orgs_data = user_data.get("orgs", [])

    orgs = (
        [
            OAuthOrgInfo(
                sub=org.get("sub"),
                name=org.get("name"),
                preferred_username=org.get("preferred_username"),
                picture=org.get("picture"),
                plan=org.get("plan"),
                can_pay=org.get("canPay"),
                role_in_org=org.get("roleInOrg"),
                security_restrictions=org.get("securityRestrictions"),
            )
            for org in orgs_data
        ]
        if orgs_data
        else None
    )

    user_info = OAuthUserInfo(
        sub=user_data.get("sub"),
        name=user_data.get("name"),
        preferred_username=user_data.get("preferred_username"),
        email_verified=user_data.get("email_verified"),
        email=user_data.get("email"),
        picture=user_data.get("picture"),
        profile=user_data.get("profile"),
        website=user_data.get("website"),
        is_pro=user_data.get("isPro"),
        can_pay=user_data.get("canPay"),
        orgs=orgs,
    )

    return OAuthInfo(
        access_token=oauth_data.get("access_token"),
        access_token_expires_at=datetime.datetime.fromtimestamp(oauth_data.get("expires_at")),
        user_info=user_info,
        state=oauth_data.get("state"),
        scope=oauth_data.get("scope"),
    )

