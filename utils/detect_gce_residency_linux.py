
def detect_gce_residency_linux():
    """Detect Google Compute Engine residency by smbios check on Linux

    Returns:
        bool: True if the GCE product name file is detected, False otherwise.
    """
    try:
        with open(_GCE_PRODUCT_NAME_FILE, "r") as file_obj:
            content = file_obj.read().strip()

    except Exception:
        return False

    return content.startswith(_GOOGLE)

