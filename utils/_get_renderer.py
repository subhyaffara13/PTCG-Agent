
def _get_renderer(figure, print_method=None):
    """
    Get the renderer that would be used to save a `.Figure`.

    If you need a renderer without any active draw methods use
    renderer._draw_disabled to temporary patch them out at your call site.
    """
    # This is implemented by triggering a draw, then immediately jumping out of
    # Figure.draw() by raising an exception.

    class Done(Exception):
        pass

    def _draw(renderer): raise Done(renderer)

    with cbook._setattr_cm(figure, draw=_draw), ExitStack() as stack:
        if print_method is None:
            fmt = figure.canvas.get_default_filetype()
            # Even for a canvas' default output type, a canvas switch may be
            # needed, e.g. for FigureCanvasBase.
            print_method = stack.enter_context(
                figure.canvas._switch_canvas_and_return_print_method(fmt))
        try:
            print_method(io.BytesIO())
        except Done as exc:
            renderer, = exc.args
            return renderer
        else:
            raise RuntimeError(f"{print_method} did not call Figure.draw, so "
                               f"no renderer is available")

