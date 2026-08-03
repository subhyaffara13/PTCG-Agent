from typing import List, Optional

def get_role_based_models(
    rbac_role: RBAC_ROLES,
    general_settings: dict,
) -> Optional[List[str]]:
    """
    Get the models allowed for a user role.

    Used by JWT Auth.
    """

    return _get_role_based_permissions(
        rbac_role=rbac_role,
        general_settings=general_settings,
        key="models",
    )

