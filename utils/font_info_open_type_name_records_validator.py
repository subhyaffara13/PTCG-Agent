from typing import Any

def fontInfoOpenTypeNameRecordsValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    if not isinstance(value, list):
        return False
    dictPrototype: GenericDict = dict(
        nameID=(int, True),
        platformID=(int, True),
        encodingID=(int, True),
        languageID=(int, True),
        string=(str, True),
    )
    for nameRecord in value:
        if not genericDictValidator(nameRecord, dictPrototype):
            return False
    return True

