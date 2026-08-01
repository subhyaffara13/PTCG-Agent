
def _validate_indices(key, self_shape, self_format):
    """Returns four sequences: (index, requested shape, arrays, nones)

    index : tuple of validated idx objects. bool arrays->nonzero(),
            arrays broadcast, ints and slices as they are, Nones removed
    requested shape : the shape of the indexed space, including Nones
    arr_pos : position within index of all arrays or ints (for array fancy indexing)
    none_pos : insert positions to put newaxis coords in indexed space.
    """
    self_ndim = len(self_shape)
    # single ellipsis
    if key is Ellipsis:
        return (slice(None),) * self_ndim, self_shape, [], []

    if not isinstance(key, tuple):
        key = [key]

    # pass 1:
    # - expand ellipsis to allow matching to self_shape
    # - preprocess boolean array index
    # - error on sparse array as an index
    # - count the ndim of the index and check if too long
    ellps_pos = None
    index_1st = []
    prelim_ndim = 0
    for i, idx in enumerate(key):
        if idx is Ellipsis:
            if ellps_pos is not None:
                raise IndexError('an index can only have a single ellipsis')
            ellps_pos = i
        elif idx is None:
            index_1st.append(idx)
        elif isinstance(idx, slice) or isintlike(idx):
            index_1st.append(idx)
            prelim_ndim += 1
        elif (ix := _compatible_boolean_index(idx, self_ndim)) is not None:
            # can't check the shape of ix until we resolve ellipsis (pass 2)
            index_1st.append(ix)
            prelim_ndim += ix.ndim
        elif issparse(idx):
            # TODO: make sparse indexing work for sparray
            raise IndexError(
                'Indexing with sparse matrices is not supported '
                'except boolean indexing where matrix and index '
                'are equal shapes.')
        else:  # dense array
            index_1st.append(np.asarray(idx))
            prelim_ndim += 1
    if prelim_ndim > self_ndim:
        raise IndexError(
            'Too many indices for array or tuple index out of range. '
            f'Key {key} needs {prelim_ndim}D. Array is {self_ndim}D'
        )
    ellip_slices = (self_ndim - prelim_ndim) * [slice(None)]
    if ellip_slices:
        if ellps_pos is None:
            index_1st.extend(ellip_slices)
        else:
            index_1st = index_1st[:ellps_pos] + ellip_slices + index_1st[ellps_pos:]

    # second pass (have processed ellipsis and preprocessed arrays)
    # pass 2:
    # note: integer arrays provide info for one axis even if >1D array.
    #       The shape of array affects outgoing(get)/incoming(set) shape only
    # - form `new_shape` (shape of outgo/incom-ing result of key
    # - form `index` (validated form of each slice/int/array index)
    # - validate and make canonical: slice and int
    # - turn bool arrays to int arrays via `.nonzero()`
    # - collect positions of Newaxis/None in `none_positions`
    # - collect positions of "array or int" in `arr_int_pos`
    idx_shape = []
    index_ndim = 0
    index = []
    array_indices = []
    none_positions = []
    arr_int_pos = []  # track positions of arrays and integers

    for i, idx in enumerate(index_1st):
        if idx is None:
            none_positions.append(len(idx_shape))
            idx_shape.append(1)
        elif isinstance(idx, slice):
            index.append(idx)
            Ms = self_shape[index_ndim]
            len_slice = len(range(*idx.indices(Ms)))
            idx_shape.append(len_slice)
            index_ndim += 1
        elif isintlike(idx):
            N = self_shape[index_ndim]
            if not (-N <= idx < N):
                raise IndexError(f'index ({idx}) out of range')
            idx = int(idx + N if idx < 0 else idx)
            index.append(idx)
            arr_int_pos.append(index_ndim)
            index_ndim += 1
        # bool array (checked in first pass)
        elif idx.dtype.kind == 'b':
            tmp_ndim = index_ndim + idx.ndim
            mid_shape = self_shape[index_ndim:tmp_ndim]
            if idx.shape != mid_shape:
                raise IndexError(
                    f"bool index {i} has shape {mid_shape} instead of {idx.shape}"
                )
            index.extend(idx.nonzero())
            array_indices.extend(range(index_ndim, tmp_ndim))
            arr_int_pos.extend(range(index_ndim, tmp_ndim))
            index_ndim = tmp_ndim
        else:  # dense array
            N = self_shape[index_ndim]
            idx = _asindices(idx, N, self_format)
            index.append(idx)
            arr_int_pos.append(index_ndim)
            array_indices.append(index_ndim)
            index_ndim += 1
    if len(array_indices) > 1:
        arr_shapes = [index[i].shape for i in array_indices]
        try:
            arr_shape = np.broadcast_shapes(*arr_shapes)
        except ValueError:
            shapes = " ".join(str(shp) for shp in arr_shapes)
            msg = (f'shape mismatch: indexing arrays could not be broadcast '
                   f'together with shapes {shapes}')
            raise IndexError(msg)
        # len(array_indices) implies arr_int_pos has at least one element
        # if arrays and ints not adjacent, move to front of shape
        if len(arr_int_pos) != (arr_int_pos[-1] - arr_int_pos[0] + 1):
            idx_shape = list(arr_shape) + idx_shape
        else:
            arr_pos = arr_int_pos[0]
            idx_shape = idx_shape[:arr_pos] + list(arr_shape) + idx_shape[arr_pos:]
    elif len(array_indices) == 1:
        arr_shape = index[array_indices[0]].shape
        arr_pos = arr_int_pos[0]
        idx_shape = idx_shape[:arr_pos] + list(arr_shape) + idx_shape[arr_pos:]
    return tuple(index), tuple(idx_shape), arr_int_pos, none_positions

