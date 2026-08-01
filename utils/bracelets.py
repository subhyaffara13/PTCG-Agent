
def bracelets(n, k):
    """Wrapper to necklaces to return a free (unrestricted) necklace."""
    return necklaces(n, k, free=True)

