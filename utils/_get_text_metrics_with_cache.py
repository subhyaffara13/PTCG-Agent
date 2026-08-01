
def _get_text_metrics_with_cache(renderer, text, fontprop, ismath, dpi):
    """Call ``renderer.get_text_width_height_descent``, caching the results."""

    # hit the outer cache layer and get the function to compute the metrics
    # for this renderer instance
    get_text_metrics = _get_text_metrics_function(renderer)
    # call the function to compute the metrics and return
    #
    # We pass a copy of the fontprop because FontProperties is both mutable and
    # has a `__hash__` that depends on that mutable state.  This is not ideal
    # as it means the hash of an object is not stable over time which leads to
    # very confusing behavior when used as keys in dictionaries or hashes.
    return get_text_metrics(text, fontprop.copy(), ismath, dpi)

