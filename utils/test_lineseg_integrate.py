
def test_lineseg_integrate():
    polygon = [(0, 5, 0), (5, 5, 0), (5, 5, 5), (0, 5, 5)]
    line_seg = [(0, 5, 0), (5, 5, 0)]
    assert lineseg_integrate(polygon, 0, line_seg, 1, 0) == 5
    assert lineseg_integrate(polygon, 0, line_seg, 0, 0) == 0

