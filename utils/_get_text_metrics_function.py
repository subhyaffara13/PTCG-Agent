import functools

def _get_text_metrics_function(input_renderer, _cache=weakref.WeakKeyDictionary()):
    """
    Helper function to provide a two-layered cache for font metrics


    To get the rendered size of a size of string we need to know:
      - what renderer we are using
      - the current dpi of the renderer
      - the string
      - the font properties
      - is it math text or not

    We do this as a two-layer cache with the outer layer being tied to a
    renderer instance and the inner layer handling everything else.

    The outer layer is implemented as `.WeakKeyDictionary` keyed on the
    renderer.  As long as someone else is holding a hard ref to the renderer
    we will keep the cache alive, but it will be automatically dropped when
    the renderer is garbage collected.

    The inner layer is provided by an lru_cache with a large maximum size (such
    that we expect very few cache misses in actual use cases).  As the
    dpi is mutable on the renderer, we need to explicitly include it as part of
    the cache key on the inner layer even though we do not directly use it (it is
    used in the method call on the renderer).

    This function takes a renderer and returns a function that can be used to
    get the font metrics.

    Parameters
    ----------
    input_renderer : maplotlib.backend_bases.RendererBase
        The renderer to set the cache up for.

    _cache : dict, optional
        We are using the mutable default value to attach the cache to the function.

        In principle you could pass a different dict-like to this function to inject
        a different cache, but please don't.  This is an internal function not meant to
        be reused outside of the narrow context we need it for.

        There is a possible race condition here between threads, we may need to drop the
        mutable default and switch to a threadlocal variable in the future.

    """
    if (_text_metrics := _cache.get(input_renderer, None)) is None:
        # We are going to include this in the closure we put as values in the
        # cache.  Closing over a hard-ref would create an unbreakable reference
        # cycle.
        renderer_ref = weakref.ref(input_renderer)

        # define the function locally to get a new lru_cache per renderer
        @functools.lru_cache(4096)
        # dpi is unused, but participates in cache invalidation (via the renderer).
        def _text_metrics(text, fontprop, ismath, dpi):
            # this should never happen under normal use, but this is a better error to
            # raise than an AttributeError on `None`
            if (local_renderer := renderer_ref()) is None:
                raise RuntimeError(
                    "Trying to get text metrics for a renderer that no longer exists.  "
                    "This should never happen and is evidence of a bug elsewhere."
                    )
            # do the actual method call we need and return the result
            return local_renderer.get_text_width_height_descent(text, fontprop, ismath)

        # stash the function for later use.
        _cache[input_renderer] = _text_metrics

    # return the inner function
    return _text_metrics

