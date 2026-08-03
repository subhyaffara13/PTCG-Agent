from typing import Dict, Optional

def get_callback_config(callback_name: str) -> Optional[Dict]:
    """
    Get the configuration for a specific callback

    Args:
        callback_name: Name of the callback to get config for

    Returns:
        Optional[Dict]: Configuration dict for the callback, or None if not found
    """
    compatible_callbacks = load_compatible_callbacks()
    return compatible_callbacks.get(callback_name)

