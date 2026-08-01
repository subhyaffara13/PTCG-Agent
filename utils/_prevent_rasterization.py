
def _prevent_rasterization(draw):
    # We assume that by default artists are not allowed to rasterize (unless
    # its draw method is explicitly decorated). If it is being drawn after a
    # rasterized artist and it has reached a raster_depth of 0, we stop
    # rasterization so that it does not affect the behavior of normal artist
    # (e.g., change in dpi).

    @wraps(draw)
    def draw_wrapper(artist, renderer, *args, **kwargs):
        if renderer._raster_depth == 0 and renderer._rasterizing:
            # Only stop when we are not in a rasterized parent
            # and something has been rasterized since last stop.
            renderer.stop_rasterizing()
            renderer._rasterizing = False

        return draw(artist, renderer, *args, **kwargs)

    draw_wrapper._supports_rasterization = False
    return draw_wrapper

