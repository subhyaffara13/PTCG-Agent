
def _checkSubstitutionGlyphsExist(glyphNames, substitutions):
    referencedGlyphNames = set()
    for _, substitution in substitutions:
        referencedGlyphNames |= substitution.keys()
        referencedGlyphNames |= set(substitution.values())
    missing = referencedGlyphNames - glyphNames
    if missing:
        raise VarLibValidationError(
            "Missing glyphs are referenced in conditional substitution rules:"
            f" {', '.join(missing)}"
        )

