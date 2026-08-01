
def build_shapes(string: str, dimension_dict: Optional[Dict[str, int]] = None) -> Tuple[TensorShapeType, ...]:
    """Builds random tensor shapes for testing.

    Parameters:
        string: List of tensor strings to build
        dimension_dict: Dictionary of index sizes, defaults to indices size of 2-7

    Returns:
        The resulting shapes.

    Examples:
        ```python
        >>> shapes = build_shapes('abbc', {'a': 2, 'b':3, 'c':5})
        >>> shapes
        [(2, 3), (3, 3, 5), (5,)]
        ```

    """
    if dimension_dict is None:
        dimension_dict = _default_dim_dict

    shapes = []
    terms = string.split("->")[0].split(",")
    for term in terms:
        dims = [dimension_dict[x] for x in term]
        shapes.append(tuple(dims))
    return tuple(shapes)

