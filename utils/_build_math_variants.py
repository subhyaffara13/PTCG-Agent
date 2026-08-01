
def _buildMathVariants(
    glyphMap,
    minConnectorOverlap,
    vertGlyphVariants,
    horizGlyphVariants,
    vertGlyphAssembly,
    horizGlyphAssembly,
):
    if not any(
        [vertGlyphVariants, horizGlyphVariants, vertGlyphAssembly, horizGlyphAssembly]
    ):
        return None

    variants = ot.MathVariants()
    variants.populateDefaults()

    variants.MinConnectorOverlap = minConnectorOverlap

    if vertGlyphVariants or vertGlyphAssembly:
        variants.VertGlyphCoverage, variants.VertGlyphConstruction = (
            _buildMathGlyphConstruction(
                glyphMap,
                vertGlyphVariants,
                vertGlyphAssembly,
            )
        )

    if horizGlyphVariants or horizGlyphAssembly:
        variants.HorizGlyphCoverage, variants.HorizGlyphConstruction = (
            _buildMathGlyphConstruction(
                glyphMap,
                horizGlyphVariants,
                horizGlyphAssembly,
            )
        )

    return variants

