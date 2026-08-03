from typing import Optional

def get_litellm_user_role(role_str) -> Optional[LitellmUserRoles]:
    """
    Convert a string (or list of strings) to a LitellmUserRoles enum if valid (case-insensitive).

    Handles list inputs since some SSO providers (e.g., Keycloak) return roles
    as arrays like ["proxy_admin"] instead of plain strings.

    Args:
        role_str: String or list to convert (e.g., "proxy_admin", ["proxy_admin"])

    Returns:
        LitellmUserRoles enum if valid, None otherwise
    """
    try:
        if isinstance(role_str, list):
            if len(role_str) == 0:
                return None
            role_str = role_str[0]
        # Use _value2member_map_ for O(1) lookup, case-insensitive
        result = LitellmUserRoles._value2member_map_.get(role_str.lower())
        return cast(Optional[LitellmUserRoles], result)
    except Exception:
        return None

