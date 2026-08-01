
def _user_is_org_admin(
    request_data: dict,
    user_object: Optional[LiteLLM_UserTable] = None,
) -> bool:
    """
    Helper function to check if user is an org admin for all of the passed organizations.

    Checks both:
    - `organization_id` (singular string) — legacy callers
    - `organizations` (list of strings) — used by /user/new
    """
    if user_object is None:
        return False

    if user_object.organization_memberships is None:
        return False

    # Collect candidate org IDs from both fields
    candidate_org_ids: List[str] = []
    singular = request_data.get("organization_id", None)
    if singular is not None:
        candidate_org_ids.append(singular)
    orgs_list = request_data.get("organizations", None)
    if isinstance(orgs_list, list):
        candidate_org_ids.extend(orgs_list)

    if not candidate_org_ids:
        return False

    # Build set of orgs where user is admin
    admin_org_ids = {
        _membership.organization_id
        for _membership in user_object.organization_memberships
        if _membership.user_role == LitellmUserRoles.ORG_ADMIN.value
        and _membership.organization_id is not None
    }

    # User must be admin of ALL requested orgs, not just any one
    return all(org_id in admin_org_ids for org_id in candidate_org_ids)

