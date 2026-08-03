import os
from typing import Optional

def get_ui_credentials(master_key: Optional[str]) -> tuple[str, str]:
    """
    Get UI username and password from environment variables or master key.

    Args:
        master_key: Master key for the proxy (used as fallback for password)

    Returns:
        tuple[str, str]: A tuple containing (ui_username, ui_password)

    Raises:
        ProxyException: If neither UI_PASSWORD nor master_key is available
    """
    ui_username = os.getenv("UI_USERNAME", "admin")
    ui_password = os.getenv("UI_PASSWORD", None)
    if ui_password is None:
        ui_password = str(master_key) if master_key is not None else None
    if ui_password is None:
        raise ProxyException(
            message="set Proxy master key to use UI. https://docs.litellm.ai/docs/proxy/virtual_keys. If set, use `--detailed_debug` to debug issue.",
            type=ProxyErrorTypes.auth_error,
            param="UI_PASSWORD",
            code=500,
        )
    return ui_username, ui_password

