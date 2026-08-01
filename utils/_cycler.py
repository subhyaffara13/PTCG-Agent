
def _cycler(label: K, itr: Iterable[V]) -> Cycler[K, V]:
    """
    Create a new `Cycler` object from a property name and iterable of values.

    Parameters
    ----------
    label : hashable
        The property key.
    itr : iterable
        Finite length iterable of the property values.

    Returns
    -------
    cycler : Cycler
        New `Cycler` for the given property
    """
    if isinstance(itr, Cycler):
        keys = itr.keys
        if len(keys) != 1:
            msg = "Can not create Cycler from a multi-property Cycler"
            raise ValueError(msg)

        lab = keys.pop()
        # Doesn't need to be a new list because
        # _from_iter() will be creating that new list anyway.
        itr = (v[lab] for v in itr)

    return Cycler._from_iter(label, itr)

