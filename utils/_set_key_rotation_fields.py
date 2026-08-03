from typing import Optional

def _set_key_rotation_fields(
    data: dict,
    auto_rotate: bool,
    rotation_interval: Optional[str],
    existing_key_alias: Optional[str] = None,
) -> None:
    """
    Helper function to set rotation fields in key data if auto_rotate is enabled.

    Args:
        data: Dictionary to update with rotation fields
        auto_rotate: Whether auto rotation is enabled
        rotation_interval: The rotation interval string (required if auto_rotate is True)
        existing_key_alias: The existing key alias from the database (if any)
    """
    if auto_rotate and rotation_interval:
        if (
            litellm._key_management_settings is not None
            and litellm._key_management_settings.store_virtual_keys is True
            and data.get("key_alias") is None
            and existing_key_alias is None
        ):
            raise ProxyException(
                message="key_alias is required when auto_rotate=True and store_virtual_keys is enabled. This ensures stable secret naming during rotation.",
                type=ProxyErrorTypes.bad_request_error,
                param="key_alias",
                code=400,
            )
        data.update(
            {
                "auto_rotate": auto_rotate,
                "rotation_interval": rotation_interval,
                "key_rotation_at": _calculate_key_rotation_time(rotation_interval),
            }
        )

