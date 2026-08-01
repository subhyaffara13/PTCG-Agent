
def get_audit_log_changed_by(
    *,
    litellm_changed_by: Optional[str],
    user_api_key_dict: UserAPIKeyAuth,
    litellm_proxy_admin_name: Optional[str],
) -> Optional[str]:
    if litellm_changed_by and _allows_litellm_changed_by_header(user_api_key_dict):
        return litellm_changed_by
    return user_api_key_dict.user_id or litellm_proxy_admin_name

