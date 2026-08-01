
def _get_empty_indexer() -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
    """Return empty join indexers."""
    return (
        np.array([], dtype=np.intp),
        np.array([], dtype=np.intp),
    )

