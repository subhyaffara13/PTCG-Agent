
def infer_enum(
    node: nodes.Call, context: InferenceContext | None = None
) -> Iterator[bases.Instance]:
    """Specific inference function for enum Call node."""
    # Raise `UseInferenceDefault` if `node` is a call to a a user-defined Enum.
    try:
        inferred = node.func.infer(context)
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if not any(
        isinstance(item, nodes.ClassDef) and item.qname() == ENUM_QNAME
        for item in inferred
    ):
        raise UseInferenceDefault

    enum_meta = _extract_single_node(
        """
    class EnumMeta(object):
        'docstring'
        def __call__(self, node):
            class EnumAttribute(object):
                name = ''
                value = 0
            return EnumAttribute()
        def __iter__(self):
            class EnumAttribute(object):
                name = ''
                value = 0
            return [EnumAttribute()]
        def __reversed__(self):
            class EnumAttribute(object):
                name = ''
                value = 0
            return (EnumAttribute, )
        def __next__(self):
            return next(iter(self))
        def __getitem__(self, attr):
            class Value(object):
                @property
                def name(self):
                    return ''
                @property
                def value(self):
                    return attr

            return Value()
        __members__ = ['']
    """
    )

    # FIXME arguably, the base here shouldn't be the EnumMeta class definition
    # itself, but a reference (Name) to it. Otherwise, the invariant that all
    # children of a node have that node as their parent is broken.
    class_node = infer_func_form(
        node,
        enum_meta,
        parent=SYNTHETIC_ROOT,
        context=context,
        enum=True,
    )[0]
    return iter([class_node.instantiate_class()])

