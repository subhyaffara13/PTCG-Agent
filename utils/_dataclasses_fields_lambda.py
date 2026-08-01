
def _dataclasses_fields_lambda(obj: VariableTracker) -> TupleVariable:
    value = None
    if isinstance(obj, UserDefinedObjectVariable):
        value = obj.value
    else:
        unimplemented(
            gb_type="dataclass fields failure",
            context=f"obj: {obj}; variable type: {type(obj)}",
            explanation=f"Dataclass fields handling fails for {obj}. Expected it to be a user-defined object.",
            hints=[],
        )
    assert value is not None
    items = []
    # type: ignore[arg-type]
    for field in dataclasses.fields(value):
        source = None
        if obj.source:
            base_src = AttrSource(obj.source, "__dataclass_fields__")
            source = DictGetItemSource(base_src, field.name)
        items.append(UserDefinedObjectVariable(field, source=source))
    # pyrefly: ignore [bad-argument-type]
    return TupleVariable(items)

