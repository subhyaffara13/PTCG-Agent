
def test_patheffects_overridden_methods_open_close_group():
    class CustomRenderer(RendererBase):
        def __init__(self):
            super().__init__()

        def open_group(self, s, gid=None):
            return "open_group overridden"

        def close_group(self, s):
            return "close_group overridden"

    renderer = PathEffectRenderer([path_effects.Normal()], CustomRenderer())

    assert renderer.open_group('s') == "open_group overridden"
    assert renderer.close_group('s') == "close_group overridden"

