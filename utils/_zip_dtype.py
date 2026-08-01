
def _zip_dtype(seqarrays, flatten=False):
    newdtype = []
    if flatten:
        for a in seqarrays:
            newdtype.extend(flatten_descr(a.dtype))
    else:
        for a in seqarrays:
            current = a.dtype
            if current.names is not None and len(current.names) == 1:
                # special case - dtypes of 1 field are flattened
                newdtype.extend(_get_fieldspec(current))
            else:
                newdtype.append(('', current))
    return np.dtype(newdtype)

