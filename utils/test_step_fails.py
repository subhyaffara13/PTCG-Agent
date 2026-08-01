
def test_step_fails(args):
    with pytest.raises(ValueError):
        cbook.pts_to_prestep(*args)

