
def makeGlyph(s):
    if s[:2] in ["U ", "u "]:
        return ttLib.TTFont._makeGlyphName(int(s[2:], 16))
    elif s[:2] == "# ":
        return "glyph%.5d" % int(s[2:])
    assert s.find(" ") < 0, "Space found in glyph name: %s" % s
    assert s, "Glyph name is empty"
    return s

