
def test_draw_wraper_forward_input():
    class TestKlass(martist.Artist):
        def draw(self, renderer, extra):
            return extra

    art = TestKlass()
    renderer = mbackend_bases.RendererBase()

    assert 'aardvark' == art.draw(renderer, 'aardvark')
    assert 'aardvark' == art.draw(renderer, extra='aardvark')

