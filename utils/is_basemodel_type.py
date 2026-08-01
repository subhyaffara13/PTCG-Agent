
def is_basemodel_type(type_: type) -> TypeGuard[type[BaseModel] | type[GenericModel]]:
    origin = get_origin(type_) or type_
    if not inspect.isclass(origin):
        return False
    return issubclass(origin, BaseModel) or issubclass(origin, GenericModel)


def is_basemodel_type(typ: type) -> TypeGuard[type[pydantic.BaseModel]]:
    if not inspect.isclass(typ):
        return False
    return issubclass(typ, pydantic.BaseModel)

