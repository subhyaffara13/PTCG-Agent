import os
from typing import Any, List, Optional, Union

def process_sso_jwt_access_token(
    access_token_str: Optional[str],
    sso_jwt_handler: Optional[JWTHandler],
    result: Union[OpenID, dict, None],
    role_mappings: Optional["RoleMappings"] = None,
) -> Optional[dict]:
    """
    Process SSO JWT access token and extract team IDs and user role if available.

    This function decodes the JWT access token and extracts team IDs and user
    role, then sets them on the result object. Role extraction from the access
    token is needed because some SSO providers (e.g., Keycloak) do not include
    role claims in the UserInfo endpoint response.

    Args:
        access_token_str: The JWT access token string
        sso_jwt_handler: SSO-specific JWT handler for team ID extraction
        result: The SSO result object to update with team IDs and role
        role_mappings: Optional role mappings configuration for group-based role determination

    Returns:
        The decoded access token payload dict, or None if decoding failed or
        inputs were missing. Callers can pass this to _sync_user_role_from_jwt_role_map
        so it has access to custom role claims (e.g. custom_roles) that are
        encoded inside the JWT but stripped from received_response.
    """
    if access_token_str and result:
        import jwt

        try:
            access_token_payload = jwt.decode(
                access_token_str, options={"verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            verbose_proxy_logger.debug(
                "Access token is not a valid JWT (possibly an opaque token), skipping JWT-based extraction"
            )
            return None

        # Extract team IDs from access token if sso_jwt_handler is available
        if sso_jwt_handler:
            if isinstance(result, dict):
                result_team_ids: Optional[List[str]] = result.get("team_ids", [])
                if not result_team_ids:
                    team_ids = sso_jwt_handler.get_team_ids_from_jwt(
                        access_token_payload
                    )
                    result["team_ids"] = team_ids
            else:
                result_team_ids = getattr(result, "team_ids", []) if result else []
                if not result_team_ids:
                    team_ids = sso_jwt_handler.get_team_ids_from_jwt(
                        access_token_payload
                    )
                    setattr(result, "team_ids", team_ids)

        # Extract user role from access token if not already set from UserInfo
        existing_role = (
            result.get("user_role")
            if isinstance(result, dict)
            else getattr(result, "user_role", None)
        )
        if existing_role is None:
            user_role: Optional[LitellmUserRoles] = None

            # Try role_mappings first (group-based role determination)
            if role_mappings is not None and role_mappings.roles:
                group_claim = role_mappings.group_claim
                user_groups_raw: Any = get_nested_value(
                    access_token_payload, group_claim
                )

                user_groups: List[str] = []
                if isinstance(user_groups_raw, list):
                    user_groups = [str(g) for g in user_groups_raw]
                elif isinstance(user_groups_raw, str):
                    user_groups = [
                        g.strip() for g in user_groups_raw.split(",") if g.strip()
                    ]
                elif user_groups_raw is not None:
                    user_groups = [str(user_groups_raw)]

                if user_groups:
                    user_role = determine_role_from_groups(user_groups, role_mappings)
                    verbose_proxy_logger.debug(
                        f"Determined role '{user_role}' from access token groups '{user_groups}' using role_mappings"
                    )
                elif role_mappings.default_role:
                    user_role = role_mappings.default_role

            # Fallback: try GENERIC_USER_ROLE_ATTRIBUTE on the access token payload
            if user_role is None:
                generic_user_role_attribute_name = os.getenv(
                    "GENERIC_USER_ROLE_ATTRIBUTE", "role"
                )
                user_role_from_token = get_nested_value(
                    access_token_payload, generic_user_role_attribute_name
                )
                if user_role_from_token is not None:
                    user_role = get_litellm_user_role(user_role_from_token)
                    verbose_proxy_logger.debug(
                        f"Extracted role '{user_role}' from access token field '{generic_user_role_attribute_name}'"
                    )

            if user_role is not None:
                if isinstance(result, dict):
                    result["user_role"] = user_role
                else:
                    setattr(result, "user_role", user_role)
                verbose_proxy_logger.debug(
                    f"Set user_role='{user_role}' from JWT access token"
                )

        return access_token_payload

    return None

