
def is_valid_multipart_property_def(prop: OverloadedFuncDef) -> bool:
    # Checks to ensure supported property decorator semantics
    if len(prop.items) != 2:
        return False

    getter = prop.items[0]
    setter = prop.items[1]

    return (
        isinstance(getter, Decorator)
        and isinstance(setter, Decorator)
        and getter.func.is_property
        and len(setter.decorators) == 1
        and isinstance(setter.decorators[0], MemberExpr)
        and setter.decorators[0].name == "setter"
    )

