
def _class_setstate(obj, state):
    state, slotstate = state
    registry = None
    for attrname, attr in state.items():
        if attrname == "_abc_impl":
            registry = attr
        else:
            # Note: setting attribute names on a class automatically triggers their
            # interning in CPython:
            # https://github.com/python/cpython/blob/v3.12.0/Objects/object.c#L957
            #
            # This means that to get deterministic pickling for a dynamic class that
            # was initially defined in a different Python process, the pickler
            # needs to ensure that dynamic class and function attribute names are
            # systematically copied into a non-interned version to avoid
            # unpredictable pickle payloads.
            #
            # Indeed the Pickler's memoizer relies on physical object identity to break
            # cycles in the reference graph of the object being serialized.
            setattr(obj, attrname, attr)

    if sys.version_info >= (3, 13) and "__firstlineno__" in state:
        # Set the Python 3.13+ only __firstlineno__  attribute one more time, as it
        # will be automatically deleted by the `setattr(obj, attrname, attr)` call
        # above when `attrname` is "__firstlineno__". We assume that preserving this
        # information might be important for some users and that it not stale in the
        # context of cloudpickle usage, hence legitimate to propagate. Furthermore it
        # is necessary to do so to keep deterministic chained pickling as tested in
        # test_deterministic_str_interning_for_chained_dynamic_class_pickling.
        obj.__firstlineno__ = state["__firstlineno__"]

    if registry is not None:
        for subclass in registry:
            obj.register(subclass)

    # PEP-649/749: During pickling, we excluded the __annotate_func__ attribute but it
    # will be created by Python. Subsequently, annotations will be recreated when
    # __annotations__ is accessed.

    return obj

