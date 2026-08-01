
def test_ellipse_input1() -> None:
    string = "...a->..."
    views = build_views(string)

    ein = contract(string, *views, optimize=False)
    opt = contract(views[0], [Ellipsis, 0], [Ellipsis])
    assert np.allclose(ein, opt)

