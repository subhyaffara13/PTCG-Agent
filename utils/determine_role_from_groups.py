
def determine_role_from_groups(
    user_groups: List[str],
    role_mappings: "RoleMappings",
) -> Optional[LitellmUserRoles]:
    """
    Determine the highest privilege role for a user based on their groups.

    Role hierarchy (highest to lowest):
    - proxy_admin
    - proxy_admin_viewer
    - internal_user
    - internal_user_viewer

    Args:
        user_groups: List of group names from the SSO token
        role_mappings: RoleMappings configuration object

    Returns:
        The highest privilege role found, or default_role if no matches, or None
    """
    if not role_mappings.roles:
        # No role mappings configured, return default_role
        return role_mappings.default_role

    # Role hierarchy (highest to lowest)
    role_hierarchy = [
        LitellmUserRoles.PROXY_ADMIN,
        LitellmUserRoles.PROXY_ADMIN_VIEW_ONLY,
        LitellmUserRoles.INTERNAL_USER,
        LitellmUserRoles.INTERNAL_USER_VIEW_ONLY,
    ]

    # Convert user_groups to a set for efficient lookup
    user_groups_set = set(user_groups) if isinstance(user_groups, list) else set()

    # Find the highest privilege role the user belongs to
    for role in role_hierarchy:
        if role in role_mappings.roles:
            role_groups = role_mappings.roles[role]
            if isinstance(role_groups, list) and user_groups_set.intersection(
                set(role_groups)
            ):
                verbose_proxy_logger.debug(
                    f"User groups {user_groups} matched role '{role.value}' via groups: {role_groups}"
                )
                return role

    # No matching groups found, return default_role
    verbose_proxy_logger.debug(
        f"User groups {user_groups} did not match any role mappings, using default_role: {role_mappings.default_role}"
    )
    return role_mappings.default_role

