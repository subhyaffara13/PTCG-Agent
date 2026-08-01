
def _copy_user_api_key_auth_for_cache(
    user_api_key_obj: UserAPIKeyAuth,
) -> UserAPIKeyAuth:
    copied_key_obj = user_api_key_obj.model_copy()
    copied_key_obj.budget_reservation = None
    copied_key_obj.parent_otel_span = None
    copied_key_obj.request_route = None
    return copied_key_obj

