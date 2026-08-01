
def reference_one_hot(a: npt.NDArray, num_classes: int = -1) -> npt.NDArray:
    if num_classes == -1:
        num_classes = int(np.amax(a) + 1)

    idcs = a.reshape(-1) + np.arange(0, a.size, dtype=np.int64) * num_classes
    one_hot = np.zeros((a.size, num_classes), dtype=a.dtype)
    np.put(one_hot, idcs, 1)
    return one_hot.reshape(*a.shape, -1)

