from typing import Dict, List, Optional, Tuple

def get_user_organization_info(
    user_object: LiteLLM_UserTable,
) -> Tuple[List[str], Dict[str, Optional[LitellmUserRoles]]]:
    """
    Helper function to extract user organization information.

    Args:
        user_object (LiteLLM_UserTable): The user object containing organization memberships.

    Returns:
        Tuple[List[str], Dict[str, Optional[LitellmUserRoles]]]: A tuple containing:
            - List of organization IDs the user is a member of
            - Dictionary mapping organization IDs to user roles
    """
    _user_organizations: List[str] = []
    _user_organization_role_mapping: Dict[str, Optional[LitellmUserRoles]] = {}

    if user_object.organization_memberships is not None:
        for _membership in user_object.organization_memberships:
            if _membership.organization_id is not None:
                _user_organizations.append(_membership.organization_id)
                _user_organization_role_mapping[_membership.organization_id] = _membership.user_role  # type: ignore

    return _user_organizations, _user_organization_role_mapping

