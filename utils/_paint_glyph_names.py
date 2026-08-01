
def _paint_glyph_names(paint, colr):
    result = set()

    def callback(paint):
        if paint.Format in {
            otTables.PaintFormat.PaintGlyph,
            otTables.PaintFormat.PaintColrGlyph,
        }:
            result.add(paint.Glyph)

    paint.traverse(colr, callback)
    return result

