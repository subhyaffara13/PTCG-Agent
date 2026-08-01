
def test_xypic_draw_diagram():
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
    assert drawer.draw(d, grid) == xypic_draw_diagram(d, layout="sequential")

