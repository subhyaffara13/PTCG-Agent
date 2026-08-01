
def convert_from_missing_indexer_tuple(indexer: tuple, axes: list[Index]) -> tuple:
    """
    Create a filtered indexer that doesn't have any missing indexers.
    """

    def get_indexer(_i, _idx):
        return axes[_i].get_loc(_idx["key"]) if isinstance(_idx, dict) else _idx

    return tuple(get_indexer(_i, _idx) for _i, _idx in enumerate(indexer))

