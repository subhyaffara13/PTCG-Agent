
def test_metrics_cache2():
    # dig into the signature to get the mutable default used as a cache
    renderer_cache = inspect.signature(
        mpl.text._get_text_metrics_function
    ).parameters['_cache'].default
    gc.collect()
    renderer_cache.clear()

    def helper():
        fig, ax = plt.subplots()
        fig.draw_without_rendering()
        # show we hit the outer cache
        assert len(renderer_cache) == 1
        func = renderer_cache[fig.canvas.get_renderer()]
        cache_info = func.cache_info()
        # show we hit the inner cache
        assert cache_info.currsize > 0
        assert cache_info.currsize == cache_info.misses
        assert cache_info.hits > cache_info.misses
        plt.close(fig)

    helper()
    gc.collect()
    # show the outer cache has a lifetime tied to the renderer (via the figure)
    assert len(renderer_cache) == 0

