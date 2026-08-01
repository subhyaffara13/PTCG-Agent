
def test_auto_no_rasterize():
    class Gen1(martist.Artist):
        ...

    assert 'draw' in Gen1.__dict__
    assert Gen1.__dict__['draw'] is Gen1.draw

    class Gen2(Gen1):
        ...

    assert 'draw' not in Gen2.__dict__
    assert Gen2.draw is Gen1.draw

