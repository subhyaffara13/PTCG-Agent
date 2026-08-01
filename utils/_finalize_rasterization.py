
def _finalize_rasterization(draw):
    """
    Decorator for Artist.draw method. Needed on the outermost artist, i.e.
    Figure, to finish up if the render is still in rasterized mode.
    """
    @wraps(draw)
    def draw_wrapper(artist, renderer, *args, **kwargs):
        result = draw(artist, renderer, *args, **kwargs)
        if renderer._rasterizing:
            renderer.stop_rasterizing()
            renderer._rasterizing = False
        return result
    return draw_wrapper

