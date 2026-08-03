from typing import Any

def fontInfoWOFFMetadataVendorValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = {
        "name": (str, True),
        "url": (str, False),
        "dir": (str, False),
        "class": (str, False),
    }
    if not genericDictValidator(value, dictPrototype):
        return False
    if "dir" in value and value.get("dir") not in ("ltr", "rtl"):
        return False
    return True

