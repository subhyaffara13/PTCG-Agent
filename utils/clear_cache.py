
def clear_cache() -> None:
    """Clear the kernel cache."""
    global _kernel_by_name_cache
    _kernel_by_name_cache = None


def clear_cache(datasets=None):
    """
    Cleans the SciPy datasets cache directory.

    Parameters
    ----------
    datasets : callable or list/tuple of callable or None
        Dataset whose cached files are to be removed. If None (default), all cached
        files are removed.

    Examples
    --------
    >>> from scipy import datasets
    >>> ascent_array = datasets.ascent()
    >>> ascent_array.shape
    (512, 512)
    >>> datasets.clear_cache([datasets.ascent])
    Cleaning the file ascent.dat for dataset ascent
    """
    _clear_cache(datasets)


def clear_cache():
    gc.collect()
    torch.cuda.empty_cache()


def clear_cache():
    """Clear the parse cache and the quoters cache."""
    _parse_cache.clear()
    _safe_quoters.clear()

