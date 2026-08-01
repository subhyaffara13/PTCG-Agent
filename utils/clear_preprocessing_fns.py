
def clear_preprocessing_fns(clear_defaults: bool = False):
    """Clear preprocessing functions at module level.

    Args:
        clear_defaults: If True, clears all functions including defaults.
                       If False, clears only user-added functions and re-registers defaults.
    """
    cache = get_algorithm_selector_cache()
    cache.clear_preprocessing_fns(clear_defaults)

