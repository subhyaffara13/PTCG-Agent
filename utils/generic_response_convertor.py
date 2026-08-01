
def generic_response_convertor(
    response,
    jwt_handler: JWTHandler,
    sso_jwt_handler: Optional[JWTHandler] = None,
    role_mappings: Optional["RoleMappings"] = None,
    team_mappings: Optional["TeamMappings"] = None,
) -> CustomOpenID:
    generic_user_id_attribute_name = os.getenv(
        "GENERIC_USER_ID_ATTRIBUTE", "preferred_username"
    )
    generic_user_display_name_attribute_name = os.getenv(
        "GENERIC_USER_DISPLAY_NAME_ATTRIBUTE", "sub"
    )
    generic_user_email_attribute_name = os.getenv(
        "GENERIC_USER_EMAIL_ATTRIBUTE", "email"
    )

    generic_user_first_name_attribute_name = os.getenv(
        "GENERIC_USER_FIRST_NAME_ATTRIBUTE", "first_name"
    )
    generic_user_last_name_attribute_name = os.getenv(
        "GENERIC_USER_LAST_NAME_ATTRIBUTE", "last_name"
    )

    generic_provider_attribute_name = os.getenv(
        "GENERIC_USER_PROVIDER_ATTRIBUTE", "provider"
    )

    generic_user_role_attribute_name = os.getenv("GENERIC_USER_ROLE_ATTRIBUTE", "role")

    generic_user_extra_attributes = os.getenv("GENERIC_USER_EXTRA_ATTRIBUTES", None)

    verbose_proxy_logger.debug(
        f" generic_user_id_attribute_name: {generic_user_id_attribute_name}\n generic_user_email_attribute_name: {generic_user_email_attribute_name}"
    )

    all_teams = []
    if sso_jwt_handler is not None:
        team_ids = sso_jwt_handler.get_all_jwt_team_ids(cast(dict, response))
        all_teams.extend(team_ids)

    if team_mappings is not None and team_mappings.team_ids_jwt_field is not None:
        team_ids_from_db_mapping: Optional[List[str]] = get_nested_value(
            data=cast(dict, response),
            key_path=team_mappings.team_ids_jwt_field,
            default=[],
        )
        if team_ids_from_db_mapping:
            all_teams.extend(team_ids_from_db_mapping)
            verbose_proxy_logger.debug(
                f"Loaded team_ids from DB team_mappings.team_ids_jwt_field='{team_mappings.team_ids_jwt_field}': {team_ids_from_db_mapping}"
            )
    else:
        team_ids = jwt_handler.get_all_jwt_team_ids(cast(dict, response))
        all_teams.extend(team_ids)

    # Determine user role based on role_mappings if available
    # Only apply role_mappings for GENERIC SSO provider
    user_role: Optional[LitellmUserRoles] = None

    if role_mappings is not None and role_mappings.provider.lower() in [
        "generic",
        "okta",
    ]:
        # Use role_mappings to determine role from groups
        group_claim = role_mappings.group_claim
        user_groups_raw: Any = get_nested_value(response, group_claim)

        # Handle different formats: could be a list, string (comma-separated), or single value
        user_groups: List[str] = []
        if isinstance(user_groups_raw, list):
            user_groups = [str(g) for g in user_groups_raw]
        elif isinstance(user_groups_raw, str):
            # Handle comma-separated string
            user_groups = [g.strip() for g in user_groups_raw.split(",") if g.strip()]
        elif user_groups_raw is not None:
            # Single value
            user_groups = [str(user_groups_raw)]

        if user_groups:
            user_role = determine_role_from_groups(user_groups, role_mappings)
            verbose_proxy_logger.debug(
                f"Determined role '{user_role.value if user_role else None}' from groups '{user_groups}' using role_mappings"
            )
        else:
            # No groups found, use default_role
            user_role = role_mappings.default_role
            verbose_proxy_logger.debug(
                f"No groups found in '{group_claim}', using default_role: {role_mappings.default_role}"
            )

    # Fallback to existing logic if role_mappings not used
    if user_role is None:
        user_role_from_sso = get_nested_value(
            response, generic_user_role_attribute_name
        )
        if user_role_from_sso is not None:
            role = get_litellm_user_role(user_role_from_sso)
            if role is not None:
                user_role = role
                verbose_proxy_logger.debug(
                    f"Found valid LitellmUserRoles '{role.value}' from SSO attribute '{generic_user_role_attribute_name}'"
                )

    # Build extra_fields dict from GENERIC_USER_EXTRA_ATTRIBUTES if specified
    extra_fields: Optional[Dict[str, Any]] = None
    if generic_user_extra_attributes:
        extra_fields = {}
        for attr_name in generic_user_extra_attributes.split(","):
            attr_name = attr_name.strip()
            extra_fields[attr_name] = get_nested_value(response, attr_name)

    return CustomOpenID(
        id=get_nested_value(response, generic_user_id_attribute_name),
        display_name=get_nested_value(
            response, generic_user_display_name_attribute_name
        ),
        email=normalize_email(
            get_nested_value(response, generic_user_email_attribute_name)
        ),
        first_name=get_nested_value(response, generic_user_first_name_attribute_name),
        last_name=get_nested_value(response, generic_user_last_name_attribute_name),
        provider=get_nested_value(response, generic_provider_attribute_name),
        team_ids=all_teams,
        user_role=user_role,
        extra_fields=extra_fields,
    )

