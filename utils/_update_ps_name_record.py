import re

def _updatePSNameRecord(varfont, familyName, styleName, platform):
    # Implementation based on Adobe Technical Note #5902 :
    # https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5902.AdobePSNameGeneration.pdf
    nametable = varfont["name"]

    family_prefix = nametable.getName(
        NameID.VARIATIONS_POSTSCRIPT_NAME_PREFIX, *platform
    )
    if family_prefix:
        family_prefix = family_prefix.toUnicode()
    else:
        family_prefix = familyName

    psName = f"{family_prefix}-{styleName}"
    # Remove any characters other than uppercase Latin letters, lowercase
    # Latin letters, digits and hyphens.
    psName = re.sub(r"[^A-Za-z0-9-]", r"", psName)

    if len(psName) > 127:
        # Abbreviating the stylename so it fits within 127 characters whilst
        # conforming to every vendor's specification is too complex. Instead
        # we simply truncate the psname and add the required "..."
        return f"{psName[:124]}..."
    return psName

