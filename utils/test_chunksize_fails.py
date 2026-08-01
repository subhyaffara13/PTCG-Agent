
def test_chunksize_fails(high_memory):
    # NOTE: This test covers multiple independent test scenarios in a single
    #       function, because each scenario uses ~2GB of memory and we don't
    #       want parallel test executors to accidentally run multiple of these
    #       at the same time.

    N = 100_000
    dpi = 500
    w = 5*dpi
    h = 6*dpi

    # make a Path that spans the whole w-h rectangle
    x = np.linspace(0, w, N)
    y = np.ones(N) * h
    y[::2] = 0
    path = Path(np.vstack((x, y)).T)
    # effectively disable path simplification (but leaving it "on")
    path.simplify_threshold = 0

    # setup the minimal GraphicsContext to draw a Path
    ra = RendererAgg(w, h, dpi)
    gc = ra.new_gc()
    gc.set_linewidth(1)
    gc.set_foreground('r')

    gc.set_hatch('/')
    with pytest.raises(OverflowError, match='cannot split hatched path'):
        ra.draw_path(gc, path, IdentityTransform())
    gc.set_hatch(None)

    with pytest.raises(OverflowError, match='cannot split filled path'):
        ra.draw_path(gc, path, IdentityTransform(), (1, 0, 0))

    # Set to zero to disable, currently defaults to 0, but let's be sure.
    with rc_context({'agg.path.chunksize': 0}):
        with pytest.raises(OverflowError, match='Please set'):
            ra.draw_path(gc, path, IdentityTransform())

    # Set big enough that we do not try to chunk.
    with rc_context({'agg.path.chunksize': 1_000_000}):
        with pytest.raises(OverflowError, match='Please reduce'):
            ra.draw_path(gc, path, IdentityTransform())

    # Small enough we will try to chunk, but big enough we will fail to render.
    with rc_context({'agg.path.chunksize': 90_000}):
        with pytest.raises(OverflowError, match='Please reduce'):
            ra.draw_path(gc, path, IdentityTransform())

    path.should_simplify = False
    with pytest.raises(OverflowError, match="should_simplify is False"):
        ra.draw_path(gc, path, IdentityTransform())

