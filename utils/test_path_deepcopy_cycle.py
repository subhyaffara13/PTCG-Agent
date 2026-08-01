
def test_path_deepcopy_cycle():
    class PathWithCycle(Path):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.x = self

    p = PathWithCycle([[0, 0], [1, 1]], readonly=True)
    p_copy = p.deepcopy()
    assert p_copy is not p
    assert p.readonly
    assert not p_copy.readonly
    assert p_copy.x is p_copy

    class PathWithCycle2(Path):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.x = [self] * 2

    p2 = PathWithCycle2([[0, 0], [1, 1]], readonly=True)
    p2_copy = p2.deepcopy()
    assert p2_copy is not p2
    assert p2.readonly
    assert not p2_copy.readonly
    assert p2_copy.x[0] is p2_copy
    assert p2_copy.x[1] is p2_copy

