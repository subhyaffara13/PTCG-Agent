
def test_XypicDiagramDrawer_line():
    # A linear diagram.
    A = Object("A")
    B = Object("B")
    C = Object("C")
    D = Object("D")
    E = Object("E")

    f = NamedMorphism(A, B, "f")
    g = NamedMorphism(B, C, "g")
    h = NamedMorphism(C, D, "h")
    i = NamedMorphism(D, E, "i")
    d = Diagram([f, g, h, i])
    grid = DiagramGrid(d, layout="sequential")
    drawer = XypicDiagramDrawer()
    assert drawer.draw(d, grid) == "\\xymatrix{\n" \
        "A \\ar[r]^{f} & B \\ar[r]^{g} & C \\ar[r]^{h} & D \\ar[r]^{i} & E \n" \
        "}\n"

    # The same diagram, transposed.
    grid = DiagramGrid(d, layout="sequential", transpose=True)
    drawer = XypicDiagramDrawer()
    assert drawer.draw(d, grid) == "\\xymatrix{\n" \
        "A \\ar[d]^{f} \\\\\n" \
        "B \\ar[d]^{g} \\\\\n" \
        "C \\ar[d]^{h} \\\\\n" \
        "D \\ar[d]^{i} \\\\\n" \
        "E \n" \
        "}\n"

