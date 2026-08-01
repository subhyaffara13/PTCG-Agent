
def apply_generic_arguments(
    callable: CallableType,
    orig_types: Sequence[Type | None],
    report_incompatible_typevar_value: Callable[[CallableType, Type, str, Context], None],
    context: Context,
    skip_unsatisfied: bool = False,
) -> CallableType:
    """Apply generic type arguments to a callable type.

    For example, applying [int] to 'def [T] (T) -> T' results in
    'def (int) -> int'.

    Note that each type can be None; in this case, it will not be applied.

    If `skip_unsatisfied` is True, then just skip the types that don't satisfy type variable
    bound or constraints, instead of giving an error.
    """
    tvars = callable.variables
    assert len(orig_types) <= len(tvars)
    # Check that inferred type variable values are compatible with allowed
    # values and bounds.  Also, promote subtype values to allowed values.
    # Create a map from type variable id to target type.
    id_to_type: dict[TypeVarId, Type] = {}

    for tvar, type in zip(tvars, orig_types):
        assert not isinstance(type, PartialType), "Internal error: must never apply partial type"
        if type is None:
            continue

        target_type = get_target_type(
            tvar,
            type,
            callable,
            report_incompatible_typevar_value,
            context,
            skip_unsatisfied,
            id_to_type,
        )
        if target_type is not None:
            id_to_type[tvar.id] = target_type

    # TODO: validate arg_kinds/arg_names for ParamSpec and TypeVarTuple replacements,
    # not just type variable bounds above.
    param_spec = callable.param_spec()
    if param_spec is not None:
        nt = id_to_type.get(param_spec.id)
        if nt is not None:
            # ParamSpec expansion is special-cased, so we need to always expand callable
            # as a whole, not expanding arguments individually.
            callable = expand_type(callable, id_to_type)
            assert isinstance(callable, CallableType)
            return callable.copy_modified(
                variables=[tv for tv in tvars if tv.id not in id_to_type]
            )

    # Apply arguments to argument types.
    var_arg = callable.var_arg()
    if var_arg is not None and isinstance(var_arg.typ, UnpackType):
        # Same as for ParamSpec, callable with variadic types needs to be expanded as a whole.
        callable = expand_type(callable, id_to_type)
        assert isinstance(callable, CallableType)
        return callable.copy_modified(variables=[tv for tv in tvars if tv.id not in id_to_type])
    else:
        callable = callable.copy_modified(
            arg_types=[expand_type(at, id_to_type) for at in callable.arg_types]
        )

    # Apply arguments to TypeGuard and TypeIs if any.
    if callable.type_guard is not None:
        type_guard = expand_type(callable.type_guard, id_to_type)
    else:
        type_guard = None
    if callable.type_is is not None:
        type_is = expand_type(callable.type_is, id_to_type)
    else:
        type_is = None

    # The callable may retain some type vars if only some were applied.
    # TODO: move apply_poly() logic here when new inference
    # becomes universally used (i.e. in all passes + in unification).
    # With this new logic we can actually *add* some new free variables.
    remaining_tvars: list[TypeVarLikeType] = []
    for tv in tvars:
        if tv.id in id_to_type:
            continue
        if not tv.has_default():
            remaining_tvars.append(tv)
            continue
        # TypeVarLike isn't in id_to_type mapping.
        # Only expand the TypeVar default here.
        typ = expand_type(tv, id_to_type)
        assert isinstance(typ, TypeVarLikeType)
        remaining_tvars.append(typ)

    instance_type = None
    if callable.instance_type is not None:
        instance_type = expand_type(callable.instance_type, id_to_type)
        assert isinstance(instance_type, ProperType)

    return callable.copy_modified(
        ret_type=expand_type(callable.ret_type, id_to_type),
        variables=remaining_tvars,
        type_guard=type_guard,
        type_is=type_is,
        instance_type=instance_type,
    )

