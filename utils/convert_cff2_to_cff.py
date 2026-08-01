
def convertCFF2ToCFF(font, *, updatePostTable=True):
    if "CFF2" not in font:
        raise ValueError("Input font does not contain a CFF2 table.")
    cff = font["CFF2"].cff
    _convertCFF2ToCFF(cff, font)
    del font["CFF2"]
    table = font["CFF "] = newTable("CFF ")
    table.cff = cff

    if updatePostTable and "post" in font:
        # Only version supported for fonts with CFF table is 0x00030000 not 0x20000
        post = font["post"]
        if post.formatType == 2.0:
            post.formatType = 3.0

