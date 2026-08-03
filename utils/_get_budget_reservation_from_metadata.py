from typing import Optional

def _get_budget_reservation_from_metadata(metadata: dict) -> Optional[dict]:
    metadata_budget_reservation = metadata.get("user_api_key_budget_reservation")
    if isinstance(metadata_budget_reservation, dict):
        return metadata_budget_reservation

    user_api_key_auth_obj = metadata.get("user_api_key_auth")
    if user_api_key_auth_obj is None:
        return None
    if isinstance(user_api_key_auth_obj, dict):
        budget_reservation = user_api_key_auth_obj.get("budget_reservation")
        return budget_reservation if isinstance(budget_reservation, dict) else None
    return getattr(user_api_key_auth_obj, "budget_reservation", None)

