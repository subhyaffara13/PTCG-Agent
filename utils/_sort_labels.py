
def _sort_labels(
    uniques: np.ndarray, left: npt.NDArray[np.intp], right: npt.NDArray[np.intp]
) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
    llength = len(left)
    labels = np.concatenate([left, right])

    _, new_labels = algos.safe_sort(uniques, labels, use_na_sentinel=True)
    new_left, new_right = new_labels[:llength], new_labels[llength:]

    return new_left, new_right

