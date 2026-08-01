
def get_role_based_routes(
    rbac_role: RBAC_ROLES,
    general_settings: dict,
) -> Optional[List[str]]:
    """
    Get the routes allowed for a user role.
    """

    return _get_role_based_permissions(
        rbac_role=rbac_role,
        general_settings=general_settings,
        key="routes",
    )

