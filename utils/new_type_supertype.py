
def new_type_supertype(type_: Type[Any]) -> Type[Any]:
    while hasattr(type_, '__supertype__'):
        type_ = type_.__supertype__
    return type_

