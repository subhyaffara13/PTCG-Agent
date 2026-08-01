
def _class_getstate(obj):
    clsdict = _extract_class_dict(obj)
    clsdict.pop("__weakref__", None)

    if issubclass(type(obj), abc.ABCMeta):
        # If obj is an instance of an ABCMeta subclass, don't pickle the
        # cache/negative caches populated during isinstance/issubclass
        # checks, but pickle the list of registered subclasses of obj.
        clsdict.pop("_abc_cache", None)
        clsdict.pop("_abc_negative_cache", None)
        clsdict.pop("_abc_negative_cache_version", None)
        registry = clsdict.pop("_abc_registry", None)
        if registry is None:
            # The abc caches and registered subclasses of a
            # class are bundled into the single _abc_impl attribute
            clsdict.pop("_abc_impl", None)
            (registry, _, _, _) = abc._get_dump(obj)

            clsdict["_abc_impl"] = [subclass_weakref() for subclass_weakref in registry]
        else:
            # In the above if clause, registry is a set of weakrefs -- in
            # this case, registry is a WeakSet
            clsdict["_abc_impl"] = [type_ for type_ in registry]

    if "__slots__" in clsdict:
        # pickle string length optimization: member descriptors of obj are
        # created automatically from obj's __slots__ attribute, no need to
        # save them in obj's state
        if isinstance(obj.__slots__, str):
            clsdict.pop(obj.__slots__)
        else:
            for k in obj.__slots__:
                clsdict.pop(k, None)

    clsdict.pop("__dict__", None)  # unpicklable property object

    if sys.version_info >= (3, 14):
        # PEP-649/749: __annotate_func__ contains a closure that references the class
        # dict. We need to exclude it from pickling. Python will recreate it when
        # __annotations__ is accessed at unpickling time.
        clsdict.pop("__annotate_func__", None)

    return (clsdict, {})

