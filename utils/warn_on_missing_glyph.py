
def warn_on_missing_glyph(codepoint: CharacterCodeType, fontnames: str):
    _api.warn_external(
        f"Glyph {codepoint} "
        f"({chr(codepoint).encode('ascii', 'namereplace').decode('ascii')}) "
        f"missing from font(s) {fontnames}.")

