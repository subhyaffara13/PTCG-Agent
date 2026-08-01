
def _cff_or_cff2(font):
    if "CFF " in font:
        return font["CFF "]
    return font["CFF2"]

