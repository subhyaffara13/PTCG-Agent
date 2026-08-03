from typing import Any

def fontInfoWOFFMetadataExtensionValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    dictPrototype: GenericDict = dict(
        names=(list, False), items=(list, True), id=(str, False)
    )
    if not genericDictValidator(value, dictPrototype):
        return False
    if "names" in value:
        for name in value["names"]:
            if not fontInfoWOFFMetadataExtensionNameValidator(name):
                return False
    for item in value["items"]:
        if not fontInfoWOFFMetadataExtensionItemValidator(item):
            return False
    return True

