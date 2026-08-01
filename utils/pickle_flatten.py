
def pickle_flatten(
    obj: object, cls: type[T] | tuple[type[T], ...]
) -> tuple[list[T], FlattenRest]:
    """
    Use the pickle machinery to extract objects out of an arbitrary container.

    Unlike regular ``pickle.dumps``, this function always succeeds.

    Parameters
    ----------
    obj : object
        The object to pickle.
    cls : type | tuple[type, ...]
        One or multiple classes to extract from the object.
        The instances of these classes inside ``obj`` will not be pickled.

    Returns
    -------
    instances : list[cls]
        All instances of ``cls`` found inside ``obj`` (not pickled).
    rest
        Opaque object containing the pickled bytes plus all other objects where
        ``__reduce__`` / ``__reduce_ex__`` is either not implemented or raised.
        These are unpickleable objects, types, modules, and functions.

        This object is *typically* hashable save for fairly exotic objects
        that are neither pickleable nor hashable.

        This object is pickleable if everything except ``instances`` was pickleable
        in the input object.

    See Also
    --------
    pickle_unflatten : Reverse function.

    Examples
    --------
    >>> class A:
    ...     def __repr__(self):
    ...         return "<A>"
    >>> class NS:
    ...     def __repr__(self):
    ...         return "<NS>"
    ...     def __reduce__(self):
    ...         assert False, "not serializable"
    >>> obj = {1: A(), 2: [A(), NS(), A()]}
    >>> instances, rest = pickle_flatten(obj, A)
    >>> instances
    [<A>, <A>, <A>]
    >>> pickle_unflatten(instances, rest)
    {1: <A>, 2: [<A>, <NS>, <A>]}

    This can be also used to swap inner objects; the only constraint is that
    the number of objects in and out must be the same:

    >>> pickle_unflatten(["foo", "bar", "baz"], rest)
    {1: "foo", 2: ["bar", <NS>, "baz"]}
    """
    instances: list[T] = []
    rest: list[object] = []

    class Pickler(pickle.Pickler):  # numpydoc ignore=GL08
        """
        Use the `pickle.Pickler.persistent_id` hook to extract objects.
        """

        @override
        def persistent_id(
            self, obj: object
        ) -> Literal[0, 1, None]:  # numpydoc ignore=GL08
            if isinstance(obj, cls):
                instances.append(obj)  # type: ignore[arg-type]
                return 0

            typ_ = type(obj)
            if typ_ in _BASIC_PICKLED_TYPES:  # No subclasses!
                # If obj is a collection, recursively descend inside it
                return None
            if typ_ in _BASIC_REST_TYPES:
                rest.append(obj)
                return 1

            try:
                # Note: a class that defines __slots__ without defining __getstate__
                # cannot be pickled with __reduce__(), but can with __reduce_ex__(5)
                _ = obj.__reduce_ex__(pickle.HIGHEST_PROTOCOL)
            except Exception:  # pylint: disable=broad-exception-caught
                rest.append(obj)
                return 1

            # Object can be pickled. Let the Pickler recursively descend inside it.
            return None

    f = io.BytesIO()
    p = Pickler(f, protocol=pickle.HIGHEST_PROTOCOL)
    p.dump(obj)
    return instances, (f.getvalue(), *rest)

