
def scoped_type_var_name(t: TypeVarLikeType) -> str:
    if not t.id.namespace:
        return t.name
    # TODO: support rare cases when both TypeVar name and namespace suffix coincide.
    *_, suffix = t.id.namespace.split(".")
    return f"{t.name}@{suffix}"

