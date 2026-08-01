
def _unique1d(ar, return_index=False, return_inverse=False,
              return_counts=False, *, equal_nan=True, inverse_shape=None,
              axis=None, sorted=True):
    """
    Find the unique elements of an array, ignoring shape.

    Uses a hash table to find the unique elements if possible.
    """
    ar = np.asanyarray(ar).flatten()
    if len(ar.shape) != 1:
        # np.matrix, and maybe some other array subclasses, insist on keeping
        # two dimensions for all operations. Coerce to an ndarray in such cases.
        ar = np.asarray(ar).flatten()

    optional_indices = return_index or return_inverse

    # masked arrays are not supported yet.
    if not optional_indices and not return_counts and not np.ma.is_masked(ar):
        # First we convert the array to a numpy array, later we wrap it back
        # in case it was a subclass of numpy.ndarray.
        conv = _array_converter(ar)
        ar_, = conv

        if (hash_unique := _unique_hash(ar_, equal_nan=equal_nan)) \
            is not NotImplemented:
            if sorted:
                hash_unique.sort()
            # We wrap the result back in case it was a subclass of numpy.ndarray.
            return (conv.wrap(hash_unique),)

    # If we don't use the hash map, we use the slower sorting method.
    if optional_indices:
        perm = ar.argsort(kind='mergesort' if return_index else 'quicksort')
        aux = ar[perm]
    else:
        ar.sort()
        aux = ar
    mask = np.empty(aux.shape, dtype=np.bool)
    mask[:1] = True
    if (equal_nan and aux.shape[0] > 0 and aux.dtype.kind in "cfmM" and
            np.isnan(aux[-1])):
        if aux.dtype.kind == "c":  # for complex all NaNs are considered equivalent
            aux_firstnan = np.searchsorted(np.isnan(aux), True, side='left')
        else:
            aux_firstnan = np.searchsorted(aux, aux[-1], side='left')
        if aux_firstnan > 0:
            mask[1:aux_firstnan] = (
                aux[1:aux_firstnan] != aux[:aux_firstnan - 1])
        mask[aux_firstnan] = True
        mask[aux_firstnan + 1:] = False
    else:
        mask[1:] = aux[1:] != aux[:-1]

    ret = (aux[mask],)
    if return_index:
        ret += (perm[mask],)
    if return_inverse:
        imask = np.cumsum(mask) - 1
        inv_idx = np.empty(mask.shape, dtype=np.intp)
        inv_idx[perm] = imask
        ret += (inv_idx.reshape(inverse_shape) if axis is None else inv_idx,)
    if return_counts:
        idx = np.concatenate(np.nonzero(mask) + ([mask.size],))
        ret += (np.diff(idx),)
    return ret

