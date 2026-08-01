
def expand_type_by_instance(typ: CallableType, instance: Instance) -> CallableType: ...


def expand_type_by_instance(typ: ProperType, instance: Instance) -> ProperType: ...


def expand_type_by_instance(typ: Type, instance: Instance) -> Type: ...


def expand_type_by_instance(typ: Type, instance: Instance) -> Type:
    """Substitute type variables in type using values from an Instance.
    Type variables are considered to be bound by the class declaration."""
    if not instance.args and not instance.type.has_type_var_tuple_type:
        return typ
    else:
        variables: dict[TypeVarId, Type] = {}
        if instance.type.has_type_var_tuple_type:
            assert instance.type.type_var_tuple_prefix is not None
            assert instance.type.type_var_tuple_suffix is not None

            args_prefix, args_middle, args_suffix = split_with_instance(instance)
            tvars_prefix, tvars_middle, tvars_suffix = split_with_prefix_and_suffix(
                tuple(instance.type.defn.type_vars),
                instance.type.type_var_tuple_prefix,
                instance.type.type_var_tuple_suffix,
            )
            tvar = tvars_middle[0]
            assert isinstance(tvar, TypeVarTupleType)
            variables = {tvar.id: TupleType(list(args_middle), tvar.tuple_fallback)}
            instance_args = args_prefix + args_suffix
            tvars = tvars_prefix + tvars_suffix
        else:
            tvars = tuple(instance.type.defn.type_vars)
            instance_args = instance.args

        for binder, arg in zip(tvars, instance_args):
            assert isinstance(binder, TypeVarLikeType)
            variables[binder.id] = arg

        return expand_type(typ, variables)

