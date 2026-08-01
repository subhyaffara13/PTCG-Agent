
def annotated_references(obj):
    """
    Return known information about references held by the given object.

    Returns a mapping from referents to lists of descriptions.  Note that there
    may be more than one edge leading to any particular referent; hence the
    need for a list.  Descriptions are currently strings.

    """
    references: dict[int, list[str]] = {}

    def add_reference(name, obj) -> None:
        references.setdefault(id(obj), []).append(name)

    def add_attrs(*attrs) -> None:
        for attr in attrs:
            if hasattr(obj, attr):
                add_reference(attr, getattr(obj, attr))

    def add_cell_references() -> None:
        try:
            add_attrs("cell_contents")
        except ValueError:
            # if cell_contents is empty,
            # accessing it raises ValueError
            # in this case there is no object to
            # annotate
            pass

    def add_function_references() -> None:
        add_attrs("__defaults__",
                  "__closure__",
                  "__globals__",
                  "__code__",
                  "__name__",
                  "__module__",
                  "__doc__"
                  "__qualname__",
                  "__annotations__",
                  "__kwdefaults__")


    def add_sequence_references() -> None:
        for position, item in enumerate(obj):
            add_reference(f"[{position}]", item)

    def add_dict_references() -> None:
        for key, value in obj.items():
            add_reference("key", key)
            add_reference(f"[{repr(key)}]", value)

    def add_set_references() -> None:
        for elt in obj:
            add_reference("element", elt)

    def add_bound_method_references() -> None:
        add_attrs("__self__", "__func__", "im_class")

    def add_weakref_references() -> None:
        # For subclasses of weakref, we can't reliably distinguish the
        # callback (if any) from other attributes.
        if type(obj) is weakref.ref:
            referents = gc.get_referents(obj)
            if len(referents) == 1:
                target = referents[0]
                add_reference("__callback__", target)


    def add_frame_references() -> None:
        f_locals = obj.f_locals
        add_attrs("f_back", "f_code", "f_builtins", "f_globals", "f_trace", "f_locals")
        # Some badly-behaved code replaces the f_locals dict with
        # something that doesn't support the full dict interface.  So we
        # only continue with the annotation if f_locals is a Python dict.
        if type(f_locals) is dict:
            for name, local in obj.f_locals.items():
                add_reference(f"local {name}", local)

    def add_getset_descriptor_references() -> None:
        add_attrs("__objclass__", "__name__", "__doc__")

    type_based_references = {
        tuple: add_sequence_references,
        list: add_sequence_references,
        dict: add_dict_references,
        set: add_set_references,
        frozenset: add_set_references,
        types.FunctionType: add_function_references,
        types.FrameType: add_frame_references,
        CellType: add_cell_references,
        types.MethodType: add_bound_method_references,
        weakref.ref: add_weakref_references,
        types.GetSetDescriptorType: add_getset_descriptor_references,
    }

    for type_ in type(obj).__mro__:
        if type_ in type_based_references:
            type_based_references[type_]()

    add_attrs("__dict__", "__class__")
    if isinstance(obj, type):
        add_attrs("__mro__")

    return references

