
def map_array(surface, array):
    """pygame.surfarray.map_array(Surface, array3d): return array2d

    map a 3d array into a 2d array

    Convert a 3D array into a 2D array. This will use the given Surface
    format to control the conversion.

    Note: arrays do not need to be 3D, as long as the minor axis has
    three elements giving the component colours, any array shape can be
    used (for example, a single colour can be mapped, or an array of
    colours). The array shape is limited to eleven dimensions maximum,
    including the three element minor axis.
    """
    if array.ndim == 0:
        raise ValueError("array must have at least 1 dimension")
    shape = array.shape
    if shape[-1] != 3:
        raise ValueError("array must be a 3d array of 3-value color data")
    target = numpy_empty(shape[:-1], numpy.int32)
    pix_map_array(target, array, surface)
    return target


def map_array(
    arr: ArrayLike,
    mapper,
    na_action: Literal["ignore"] | None = None,
) -> np.ndarray | ExtensionArray | Index:
    """
    Map values using an input mapping or function.

    Parameters
    ----------
    mapper : function, dict, or Series
        Mapping correspondence.
    na_action : {None, 'ignore'}, default None
        If 'ignore', propagate NA values, without passing them to the
        mapping correspondence.

    Returns
    -------
    Union[ndarray, Index, ExtensionArray]
        The output of the mapping function applied to the array.
        If the function returns a tuple with more than one element
        a MultiIndex will be returned.
    """
    from pandas import Index

    if na_action not in (None, "ignore"):
        msg = f"na_action must either be 'ignore' or None, {na_action} was passed"
        raise ValueError(msg)

    # we can fastpath dict/Series to an efficient map
    # as we know that we are not going to have to yield
    # python types
    if is_dict_like(mapper):
        if isinstance(mapper, dict) and hasattr(mapper, "__missing__"):
            # If a dictionary subclass defines a default value method,
            # convert mapper to a lookup function (GH #15999).
            dict_with_default = mapper
            mapper = lambda x: dict_with_default[
                np.nan if isinstance(x, float) and np.isnan(x) else x
            ]
        else:
            # Dictionary does not have a default. Thus it's safe to
            # convert to a Series for efficiency.
            # we specify the keys here to handle the
            # possibility that they are tuples

            # The return value of mapping with an empty mapper is
            # expected to be pd.Series(np.nan, ...). As np.nan is
            # of dtype float64 the return value of this method should
            # be float64 as well
            from pandas import Series

            if len(mapper) == 0:
                mapper = Series(mapper, dtype=np.float64)
            elif isinstance(mapper, dict):
                mapper = Series(
                    mapper.values(), index=Index(mapper.keys(), tupleize_cols=False)
                )
            else:
                mapper = Series(mapper)

    if isinstance(mapper, ABCSeries):
        if na_action == "ignore":
            mapper = mapper[mapper.index.notna()]

        # Since values were input this means we came from either
        # a dict or a series and mapper should be an index
        indexer = mapper.index.get_indexer(arr)
        new_values = take_nd(mapper._values, indexer)

        return new_values

    if not len(arr):
        return arr.copy()

    # we must convert to python types
    values = arr.astype(object, copy=False)
    if na_action is None:
        return lib.map_infer(values, mapper)
    else:
        return lib.map_infer_mask(values, mapper, mask=isna(values).view(np.uint8))

