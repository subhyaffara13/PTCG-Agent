from typing import List, Optional

def _get_role_based_permissions(
    rbac_role: RBAC_ROLES,
    general_settings: dict,
    key: Literal["models", "routes"],
) -> Optional[List[str]]:
    """
    Get the role based permissions from the general settings.
    """
    role_based_permissions = cast(
        Optional[List[RoleBasedPermissions]],
        general_settings.get("role_permissions", []),
    )
    if role_based_permissions is None:
        return None

    for role_based_permission in role_based_permissions:
        if role_based_permission.role == rbac_role:
            return getattr(role_based_permission, key)

    return None

