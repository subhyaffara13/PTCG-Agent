
def detach_callable(typ: CallableType, class_type_vars: list[TypeVarLikeType]) -> CallableType:
    """Ensures that the callable's type variables are 'detached' and independent of the context.

    A callable normally keeps track of the type variables it uses within its 'variables' field.
    However, if the callable is from a method and that method is using a class type variable,
    the callable will not keep track of that type variable since it belongs to the class.
    """
    if not class_type_vars:
        # Fast path, nothing to update.
        return typ
    return typ.copy_modified(variables=list(typ.variables) + class_type_vars)

