
def expand_type(typ: CallableType, env: Mapping[TypeVarId, Type]) -> CallableType: ...


def expand_type(typ: ProperType, env: Mapping[TypeVarId, Type]) -> ProperType: ...


def expand_type(typ: Type, env: Mapping[TypeVarId, Type]) -> Type: ...


def expand_type(typ: Type, env: Mapping[TypeVarId, Type]) -> Type:
    """Substitute any type variable references in a type given by a type
    environment.
    """
    return typ.accept(ExpandTypeVisitor(env))

