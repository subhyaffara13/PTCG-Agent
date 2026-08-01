
def _org_admin_can_invite_user(
    admin_user_obj: LiteLLM_UserTable,
    target_user_obj: LiteLLM_UserTable,
) -> bool:
    """
    Check if an org admin can invite the target user.
    Target user must be in at least one org where the admin has org admin role.

    Args:
        admin_user_obj: The admin user's full object (from get_user_object)
        target_user_obj: The target user's full object (from get_user_object)

    Returns:
        True if target user is in an org where admin has org admin role
    """
    if admin_user_obj.organization_memberships is None:
        return False
    admin_org_ids = {
        m.organization_id
        for m in admin_user_obj.organization_memberships
        if m.user_role == LitellmUserRoles.ORG_ADMIN.value
    }
    if not admin_org_ids:
        return False
    if target_user_obj.organization_memberships is None:
        return False
    target_org_ids = {
        m.organization_id for m in target_user_obj.organization_memberships
    }
    return bool(admin_org_ids & target_org_ids)

