
def _class_lookup(
    node: nodes.ClassDef, name: str, context: InferenceContext | None = None
) -> list:
    metaclass = node.metaclass(context=context)
    if metaclass is None:
        raise AttributeInferenceError(attribute=name, target=node)

    return _lookup_in_mro(metaclass, name)

