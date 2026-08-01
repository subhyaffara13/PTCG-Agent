
def test_ellipse_input3() -> None:
    string = "...a->...a"
    views = build_views(string)

    ein = contract(string, *views, optimize=False)
    opt = contract(views[0], [Ellipsis, 0], [Ellipsis, 0])
    assert np.allclose(ein, opt)

