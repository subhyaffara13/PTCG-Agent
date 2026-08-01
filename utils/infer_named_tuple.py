
def infer_named_tuple(
    node: nodes.Call, context: InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Specific inference function for namedtuple Call node."""
    tuple_base: nodes.Name = _extract_single_node("tuple")
    class_node, name, attributes = infer_func_form(
        node, tuple_base, parent=SYNTHETIC_ROOT, context=context
    )

    call_site = arguments.CallSite.from_call(node, context=context)
    func = util.safe_infer(
        _extract_single_node("import collections; collections.namedtuple")
    )
    assert isinstance(func, nodes.NodeNG)
    try:
        rename_arg_bool_value = next(
            call_site.infer_argument(func, "rename", context or InferenceContext())
        ).bool_value()
        rename = rename_arg_bool_value is True
    except (InferenceError, StopIteration):
        rename = False

    try:
        attributes = _check_namedtuple_attributes(name, attributes, rename)
    except AstroidTypeError as exc:
        raise UseInferenceDefault("TypeError: " + str(exc)) from exc
    except AstroidValueError as exc:
        raise UseInferenceDefault("ValueError: " + str(exc)) from exc

    replace_args = ", ".join(f"{arg}=None" for arg in attributes)
    field_def = (
        "    {name} = property(lambda self: self[{index:d}], "
        "doc='Alias for field number {index:d}')"
    )
    field_defs = "\n".join(
        field_def.format(name=name, index=index)
        for index, name in enumerate(attributes)
    )
    fake = AstroidBuilder(AstroidManager()).string_build(
        f"""
class {name}(tuple):
    __slots__ = ()
    _fields = {attributes!r}
    def _asdict(self):
        return self.__dict__
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        return new(cls, iterable)
    def _replace(self, {replace_args}):
        return self
    def __getnewargs__(self):
        return tuple(self)
{field_defs}
    """
    )
    class_node.locals["_asdict"] = fake.body[0].locals["_asdict"]
    class_node.locals["_make"] = fake.body[0].locals["_make"]
    class_node.locals["_replace"] = fake.body[0].locals["_replace"]
    class_node.locals["_fields"] = fake.body[0].locals["_fields"]
    for attr in attributes:
        class_node.locals[attr] = fake.body[0].locals[attr]
    # we use UseInferenceDefault, we can't be a generator so return an iterator
    return iter([class_node])

