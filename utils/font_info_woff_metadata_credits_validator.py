from typing import Any

def fontInfoWOFFMetadataCreditsValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(credits=(list, True))
    if not genericDictValidator(value, dictPrototype):
        return False
    if not len(value["credits"]):
        return False
    dictPrototype = {
        "name": (str, True),
        "url": (str, False),
        "role": (str, False),
        "dir": (str, False),
        "class": (str, False),
    }
    for credit in value["credits"]:
        if not genericDictValidator(credit, dictPrototype):
            return False
        if "dir" in credit and credit.get("dir") not in ("ltr", "rtl"):
            return False
    return True

