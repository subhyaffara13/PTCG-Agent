
def test_extract_triangulation_positional_mask():
    # mask cannot be passed positionally
    mask = [True]
    args = [[0, 2, 1], [0, 0, 1], [[0, 1, 2]], mask]
    x_, y_, triangles_, mask_, args_, kwargs_ = \
        mtri.Triangulation._extract_triangulation_params(args, {})
    assert mask_ is None
    assert args_ == [mask]

