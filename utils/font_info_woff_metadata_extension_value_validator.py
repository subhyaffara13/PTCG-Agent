from typing import Any

def fontInfoWOFFMetadataExtensionValueValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = {
        "text": (str, True),
        "language": (str, False),
        "dir": (str, False),
        "class": (str, False),
    }
    if not genericDictValidator(value, dictPrototype):
        return False
    if "dir" in value and value.get("dir") not in ("ltr", "rtl"):
        return False
    return True

