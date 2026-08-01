
def build_arrays_from_tuples(path: PathType) -> List[Any]:
    """Build random numpy arrays from a path.

    Parameters:
        path: The path to build arrays from.

    Returns:
    The resulting arrays.
    """
    np = pytest.importorskip("numpy")

    return [np.random.rand(*x) for x in path]

