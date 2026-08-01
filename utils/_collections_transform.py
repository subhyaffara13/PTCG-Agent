
def _collections_transform():
    return parse(
        """
    class defaultdict(dict):
        default_factory = None
        def __missing__(self, key): pass
        def __getitem__(self, key): return default_factory

    """
        + _deque_mock()
        + _ordered_dict_mock()
    )

