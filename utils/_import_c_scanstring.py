
def _import_c_scanstring():
    try:
        from ._speedups import scanstring
        return scanstring
    except ImportError:
        return None

