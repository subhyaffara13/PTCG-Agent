
def is_functional(op: OpOverload) -> bool:
    return not op._schema.is_mutable

