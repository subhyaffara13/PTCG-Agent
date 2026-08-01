
def _flatten_layers(lst):
    for paint in lst:
        if paint["Format"] == ot.PaintFormat.PaintColrLayers:
            yield from _flatten_layers(paint["Layers"])
        else:
            yield paint


def _flatten_layers(root, colr):
    assert root.Format == ot.PaintFormat.PaintColrLayers
    for paint in root.getChildren(colr):
        if paint.Format == ot.PaintFormat.PaintColrLayers:
            yield from _flatten_layers(paint, colr)
        else:
            yield paint

