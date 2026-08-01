
def check_remains_sorted(X):
    """Checks that sorted indices property is retained through an operation
    """
    if not hasattr(X, 'has_sorted_indices') or not X.has_sorted_indices:
        yield
        return
    yield
    indices = X.indices.copy()
    X.has_sorted_indices = False
    X.sort_indices()
    assert_array_equal(indices, X.indices,
                       'Expected sorted indices, found unsorted')


def check_remains_sorted(X):
    """Checks that sorted indices property is retained through an operation"""
    yield
    if not hasattr(X, 'has_sorted_indices') or not X.has_sorted_indices:
        return
    indices = X.indices.copy()
    X.has_sorted_indices = False
    X.sort_indices()
    assert_equal(indices, X.indices, 'Expected sorted indices, found unsorted')

