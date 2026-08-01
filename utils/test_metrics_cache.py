
def test_metrics_cache():
    # dig into the signature to get the mutable default used as a cache
    renderer_cache = inspect.signature(
        mpl.text._get_text_metrics_function
    ).parameters['_cache'].default

    renderer_cache.clear()

    fig = plt.figure()
    fig.text(.3, .5, "foo\nbar")
    fig.text(.3, .5, "foo\nbar", usetex=True)
    fig.text(.5, .5, "foo\nbar", usetex=True)
    fig.canvas.draw()
    renderer = fig._get_renderer()
    assert renderer in renderer_cache

    ys = {}  # mapping of strings to where they were drawn in y with draw_tex.

    def call(*args, **kwargs):
        renderer, x, y, s, *_ = args
        ys.setdefault(s, set()).add(y)

    renderer.draw_tex = call
    fig.canvas.draw()
    assert [*ys] == ["foo", "bar"]
    # Check that both TeX strings were drawn with the same y-position for both
    # single-line substrings.  Previously, there used to be an incorrect cache
    # collision with the non-TeX string (drawn first here) whose metrics would
    # get incorrectly reused by the first TeX string.
    assert len(ys["foo"]) == len(ys["bar"]) == 1

    info = renderer_cache[renderer].cache_info()
    # Every string gets a miss for the first layouting (extents), then a hit
    # when drawing, but "foo\nbar" gets two hits as it's drawn twice.
    assert info.hits > info.misses

