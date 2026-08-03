from typing import Union

def _addName(
    ttFont: TTFont,
    value: Union[STATName, STATNameStatement],
    minNameID: int = 0,
    windows: bool = True,
    mac: bool = True,
) -> int:
    nameTable = ttFont["name"]
    if isinstance(value, int):
        # Already a nameID
        return value
    if isinstance(value, str):
        names = dict(en=value)
    elif isinstance(value, dict):
        names = value
    elif isinstance(value, list):
        nameID = nameTable._findUnusedNameID()
        for nameRecord in value:
            if isinstance(nameRecord, STATNameStatement):
                nameTable.setName(
                    nameRecord.string,
                    nameID,
                    nameRecord.platformID,
                    nameRecord.platEncID,
                    nameRecord.langID,
                )
            else:
                raise TypeError("value must be a list of STATNameStatements")
        return nameID
    else:
        raise TypeError("value must be int, str, dict or list")
    return nameTable.addMultilingualName(
        names, ttFont=ttFont, windows=windows, mac=mac, minNameID=minNameID
    )

