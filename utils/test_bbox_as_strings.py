
def test_bbox_as_strings():
    b = mtransforms.Bbox([[.5, 0], [.75, .75]])
    assert_bbox_eq(b, eval(repr(b), {'Bbox': mtransforms.Bbox}))
    asdict = eval(str(b), {'Bbox': dict})
    for k, v in asdict.items():
        assert getattr(b, k) == v
    fmt = '.1f'
    asdict = eval(format(b, fmt), {'Bbox': dict})
    for k, v in asdict.items():
        assert eval(format(getattr(b, k), fmt)) == v

