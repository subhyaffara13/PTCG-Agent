
def _object_type_is_subclass(
    obj_type: InferenceResult | None,
    class_or_seq: list[InferenceResult],
    context: InferenceContext | None = None,
) -> util.UninferableBase | bool:
    if isinstance(obj_type, util.UninferableBase) or not isinstance(
        obj_type, nodes.ClassDef
    ):
        return util.Uninferable

    # Instances are not types
    class_seq = [
        item if not isinstance(item, bases.Instance) else util.Uninferable
        for item in class_or_seq
    ]
    # strict compatibility with issubclass
    # issubclass(type, (object, 1)) evaluates to true
    # issubclass(object, (1, type)) raises TypeError
    for klass in class_seq:
        if isinstance(klass, util.UninferableBase):
            raise AstroidTypeError(
                f"arg 2 must be a type or tuple of types, not {type(klass)!r}"
            )

        for obj_subclass in obj_type.mro():
            if obj_subclass == klass:
                return True
    return False

