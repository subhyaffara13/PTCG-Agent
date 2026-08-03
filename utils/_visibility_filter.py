from typing import List, Optional

def _visibility_filter(user_api_key_dict: UserAPIKeyAuth) -> Optional[dict]:
    """
    Prisma `where` fragment restricting rows to those the caller can see.
    Returns None for admins (no restriction).
    """
    if _is_admin(user_api_key_dict):
        return None
    ors: List[dict] = []
    if user_api_key_dict.user_id:
        ors.append({"user_id": user_api_key_dict.user_id})
    if user_api_key_dict.team_id:
        ors.append({"team_id": user_api_key_dict.team_id})
    if not ors:
        # Caller has neither user_id nor team_id — match nothing.
        return {"memory_id": "__no_match__"}
    return {"OR": ors}

