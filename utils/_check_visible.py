
def _check_visible(collections, visible=True):
    """
    Check each artist is visible or not

    Parameters
    ----------
    collections : matplotlib Artist or its list-like
        target Artist or its list or collection
    visible : bool
        expected visibility
    """
    from matplotlib.collections import Collection

    if not isinstance(collections, Collection) and not is_list_like(collections):
        collections = [collections]

    for patch in collections:
        assert patch.get_visible() == visible

