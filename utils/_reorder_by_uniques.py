
def _reorder_by_uniques(
    uniques: npt.NDArray[np.int64], labels: npt.NDArray[np.intp]
) -> tuple[npt.NDArray[np.int64], npt.NDArray[np.intp]]:
    """
    Parameters
    ----------
    uniques : np.ndarray[np.int64]
    labels : np.ndarray[np.intp]

    Returns
    -------
    np.ndarray[np.int64]
    np.ndarray[np.intp]
    """
    # sorter is index where elements ought to go
    sorter = uniques.argsort()

    # reverse_indexer is where elements came from
    reverse_indexer = np.empty(len(sorter), dtype=np.intp)
    reverse_indexer.put(sorter, np.arange(len(sorter)))

    mask = labels < 0

    # move labels to right locations (ie, unsort ascending labels)
    labels = reverse_indexer.take(labels)
    np.putmask(labels, mask, -1)

    # sort observed ids
    uniques = uniques.take(sorter)

    return uniques, labels

