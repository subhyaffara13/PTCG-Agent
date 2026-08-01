
def build_views(
    string: str, dimension_dict: Optional[Dict[str, int]] = None, array_function: Optional[Any] = None
) -> Tuple[ArrayType]:
    """Builds random numpy arrays for testing.

    Parameters:
        string: List of tensor strings to build
        dimension_dict: Dictionary of index _sizes
        array_function: Function to build the arrays, defaults to np.random.rand

    Returns:
        The resulting views.

    Examples:
        ```python
        >>> view = build_views('abbc', {'a': 2, 'b':3, 'c':5})
        >>> view[0].shape
        (2, 3, 3, 5)
        ```

    """
    if array_function is None:
        np = pytest.importorskip("numpy")
        array_function = np.random.rand

    views = []
    for shape in build_shapes(string, dimension_dict=dimension_dict):
        if shape:
            views.append(array_function(*shape))
        else:
            views.append(random.random())
    return tuple(views)


def build_views(string: str) -> List[ArrayType]:
    """Builds random numpy arrays for testing by using a fixed size dictionary and an input string."""

    chars = "abcdefghij"
    sizes_array = np.array([2, 3, 4, 5, 4, 3, 2, 6, 5, 4])
    sizes = dict(zip(chars, sizes_array))

    views = []

    string = string.replace("...", "ij")

    terms = string.split("->")[0].split(",")
    for term in terms:
        dims = [sizes[x] for x in term]
        views.append(np.random.rand(*dims))
    return views

