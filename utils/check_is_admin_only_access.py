from typing import Dict, Union

def check_is_admin_only_access(ui_access_mode: Union[str, Dict]) -> bool:
    """Checks ui access mode is admin_only"""
    if isinstance(ui_access_mode, str):
        return ui_access_mode == "admin_only"
    else:
        return False

