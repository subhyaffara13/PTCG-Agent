
def sdm_sort(f, O):
    """Sort terms in ``f`` using the given monomial order ``O``. """
    return sorted(f, key=lambda term: O(term[0]), reverse=True)

