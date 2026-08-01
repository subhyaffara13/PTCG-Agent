
def infer_constraints_for_callable(
    callee: CallableType,
    arg_types: Sequence[Type | None],
    arg_kinds: list[ArgKind],
    arg_names: Sequence[str | None] | None,
    formal_to_actual: list[list[int]],
    context: ArgumentInferContext,
) -> list[Constraint]:
    """Infer type variable constraints for a callable and actual arguments.

    Return a list of constraints.
    """
    constraints: list[Constraint] = []
    mapper = ArgTypeExpander(context)

    param_spec = callee.param_spec()
    param_spec_arg_types = []
    param_spec_arg_names = []
    param_spec_arg_kinds: list[ArgKind] = []

    incomplete_star_mapping = False
    for i, actuals in enumerate(formal_to_actual):  # TODO: isn't this `enumerate(arg_types)`?
        for actual in actuals:
            if actual is None and callee.arg_kinds[i] in (ARG_STAR, ARG_STAR2):  # type: ignore[unreachable]
                # We can't use arguments to infer ParamSpec constraint, if only some
                # are present in the current inference pass.
                incomplete_star_mapping = True  # type: ignore[unreachable]
                break

    for i, actuals in enumerate(formal_to_actual):
        if isinstance(callee.arg_types[i], UnpackType):
            unpack_type = callee.arg_types[i]
            assert isinstance(unpack_type, UnpackType)

            # In this case we are binding all the actuals to *args,
            # and we want a constraint that the typevar tuple being unpacked
            # is equal to a type list of all the actuals.
            actual_types = []

            unpacked_type = get_proper_type(unpack_type.type)
            if isinstance(unpacked_type, TypeVarTupleType):
                tuple_instance = unpacked_type.tuple_fallback
            elif isinstance(unpacked_type, TupleType):
                tuple_instance = unpacked_type.partial_fallback
            else:
                assert False, "mypy bug: unhandled constraint inference case"

            for actual in actuals:
                actual_arg_type = arg_types[actual]
                if actual_arg_type is None:
                    continue

                expanded_actual = mapper.expand_actual_type(
                    actual_arg_type,
                    arg_kinds[actual],
                    callee.arg_names[i],
                    callee.arg_kinds[i],
                    allow_unpack=True,
                )

                if arg_kinds[actual] != ARG_STAR or isinstance(
                    get_proper_type(actual_arg_type), TupleType
                ):
                    actual_types.append(expanded_actual)
                else:
                    # If we are expanding an iterable inside * actual, append a homogeneous item instead
                    actual_types.append(
                        UnpackType(tuple_instance.copy_modified(args=[expanded_actual]))
                    )

            if isinstance(unpacked_type, TypeVarTupleType):
                constraints.append(
                    Constraint(
                        unpacked_type,
                        SUPERTYPE_OF,
                        TupleType(actual_types, unpacked_type.tuple_fallback),
                    )
                )
            elif isinstance(unpacked_type, TupleType):
                # Prefixes get converted to positional args, so technically the only case we
                # should have here is like Tuple[Unpack[Ts], Y1, Y2, Y3]. If this turns out
                # not to hold we can always handle the prefixes too.
                inner_unpack = unpacked_type.items[0]
                assert isinstance(inner_unpack, UnpackType)
                inner_unpacked_type = get_proper_type(inner_unpack.type)
                suffix_len = len(unpacked_type.items) - 1
                if isinstance(inner_unpacked_type, TypeVarTupleType):
                    # Variadic item can be either *Ts...
                    constraints.append(
                        Constraint(
                            inner_unpacked_type,
                            SUPERTYPE_OF,
                            TupleType(
                                actual_types[:-suffix_len], inner_unpacked_type.tuple_fallback
                            ),
                        )
                    )
                else:
                    # ...or it can be a homogeneous tuple.
                    assert (
                        isinstance(inner_unpacked_type, Instance)
                        and inner_unpacked_type.type.fullname == "builtins.tuple"
                    )
                    for at in actual_types[:-suffix_len]:
                        constraints.extend(
                            infer_constraints(inner_unpacked_type.args[0], at, SUPERTYPE_OF)
                        )
                # Now handle the suffix (if any).
                if suffix_len:
                    for tt, at in zip(unpacked_type.items[1:], actual_types[-suffix_len:]):
                        constraints.extend(infer_constraints(tt, at, SUPERTYPE_OF))
            else:
                assert False, "mypy bug: unhandled constraint inference case"
        else:
            for actual in actuals:
                actual_arg_type = arg_types[actual]
                if actual_arg_type is None:
                    continue

                if param_spec and callee.arg_kinds[i] in (ARG_STAR, ARG_STAR2):
                    # If actual arguments are mapped to ParamSpec type, we can't infer individual
                    # constraints, instead store them and infer single constraint at the end.
                    # It is impossible to map actual kind to formal kind, so use some heuristic.
                    # This inference is used as a fallback, so relying on heuristic should be OK.
                    if not incomplete_star_mapping:
                        param_spec_arg_types.append(
                            mapper.expand_actual_type(
                                actual_arg_type, arg_kinds[actual], None, arg_kinds[actual]
                            )
                        )
                        actual_kind = arg_kinds[actual]
                        param_spec_arg_kinds.append(
                            ARG_POS if actual_kind not in (ARG_STAR, ARG_STAR2) else actual_kind
                        )
                        param_spec_arg_names.append(arg_names[actual] if arg_names else None)
                else:
                    actual_type = mapper.expand_actual_type(
                        actual_arg_type,
                        arg_kinds[actual],
                        callee.arg_names[i],
                        callee.arg_kinds[i],
                    )
                    c = infer_constraints(callee.arg_types[i], actual_type, SUPERTYPE_OF)
                    constraints.extend(c)
    if (
        param_spec
        and not any(c.type_var == param_spec.id for c in constraints)
        and not incomplete_star_mapping
    ):
        # Use ParamSpec constraint from arguments only if there are no other constraints,
        # since as explained above it is quite ad-hoc.
        constraints.append(
            Constraint(
                param_spec,
                SUPERTYPE_OF,
                Parameters(
                    arg_types=param_spec_arg_types,
                    arg_kinds=param_spec_arg_kinds,
                    arg_names=param_spec_arg_names,
                    imprecise_arg_kinds=True,
                ),
            )
        )
    if any(isinstance(v, ParamSpecType) for v in callee.variables):
        # As a perf optimization filter imprecise constraints only when we can have them.
        constraints = filter_imprecise_kinds(constraints)
    return constraints

