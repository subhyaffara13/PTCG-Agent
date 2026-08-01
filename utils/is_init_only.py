
def is_init_only(node: Var) -> bool:
    return (
        isinstance(type := get_proper_type(node.type), Instance)
        and type.type.fullname == "dataclasses.InitVar"
    )

