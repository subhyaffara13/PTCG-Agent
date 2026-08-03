from typing import Any, Optional

def _validate_caller_can_change_key_ownership(
    data: Optional[BaseModel],
    existing_key_row: Any,
    user_api_key_dict: UserAPIKeyAuth,
) -> None:
    """
    Non-admin callers must not rebind a key's ``user_id`` to a different
    user. The ``user_id`` on a verification token is what
    ``_return_user_api_key_auth_obj`` resolves against ``litellm_usertable``
    to derive the request's role; a non-admin rebinding their own key's
    ``user_id`` to a ``PROXY_ADMIN`` row promotes themselves.

    ``/key/update`` already enforces this inline; ``/key/regenerate`` did
    not. Sharing the check keeps both endpoints — and any future
    regenerate-style endpoint — consistent.
    """
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value:
        return
    if data is None:
        return
    # Distinguish "user_id omitted" from "user_id explicitly set to None".
    # Both leave ``getattr(data, 'user_id', None)`` at None, but only the
    # explicit-null variant survives ``model_dump(exclude_unset=True)`` in
    # ``prepare_key_update_data`` and writes NULL to the token row —
    # detaching the key from its user and bypassing the user-row
    # role check on subsequent requests.
    fields_set = getattr(data, "model_fields_set", None) or set()
    if "user_id" not in fields_set:
        return
    incoming_user_id = getattr(data, "user_id", None)
    if incoming_user_id is None or incoming_user_id == "":
        raise HTTPException(
            status_code=403,
            detail="Non-admin users cannot remove the user_id from a key.",
        )
    existing_user_id = getattr(existing_key_row, "user_id", None)
    if incoming_user_id != existing_user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Non-admin caller is not allowed to rebind the key from "
                f"user={existing_user_id} to user={incoming_user_id}"
            ),
        )

