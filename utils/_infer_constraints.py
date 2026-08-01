
def _infer_constraints(
    template: Type, actual: Type, direction: int, skip_neg_op: bool, erase_types: bool
) -> list[Constraint]:
    orig_template = template
    template = get_proper_type(template)
    actual = get_proper_type(actual)

    # Type inference shouldn't be affected by whether union types have been simplified.
    # We however keep any ErasedType items, so that the caller will see it when using
    # checkexpr.has_erased_component().
    if isinstance(template, UnionType):
        template = mypy.typeops.make_simplified_union(template.items, keep_erased=True)
    if isinstance(actual, UnionType):
        actual = mypy.typeops.make_simplified_union(actual.items, keep_erased=True)

    # Ignore Any types from the type suggestion engine to avoid them
    # causing us to infer Any in situations where a better job could
    # be done otherwise. (This can produce false positives but that
    # doesn't really matter because it is all heuristic anyway.)
    if isinstance(actual, AnyType) and actual.type_of_any == TypeOfAny.suggestion_engine:
        return []

    # type[A | B] is always represented as type[A] | type[B] internally.
    # This makes our constraint solver choke on type[T] <: type[A] | type[B],
    # solving T as generic meet(A, B) which is often `object`. Force unwrap such unions
    # if both sides are type[...] or unions thereof. See `testTypeVarType` test
    type_type_unwrapped = False
    if _is_type_type(template) and _is_type_type(actual):
        type_type_unwrapped = True
        template = _unwrap_type_type(template)
        actual = _unwrap_type_type(actual)

    # If the template is simply a type variable, emit a Constraint directly.
    # We need to handle this case before handling Unions for two reasons:
    #  1. "T <: Union[U1, U2]" is not equivalent to "T <: U1 or T <: U2",
    #     because T can itself be a union (notably, Union[U1, U2] itself).
    #  2. "T :> Union[U1, U2]" is logically equivalent to "T :> U1 and
    #     T :> U2", but they are not equivalent to the constraint solver,
    #     which never introduces new Union types (it uses join() instead).
    if isinstance(template, TypeVarType):
        return [Constraint(template, direction, actual)]

    if (
        isinstance(actual, TypeVarType)
        and not actual.id.is_meta_var()
        and direction == SUPERTYPE_OF
    ):
        # Unless template is also a type variable (or a union that contains one), using the upper
        # bound for inference will usually give better result for actual that is a type variable.
        if not isinstance(template, UnionType) or not any(
            isinstance(t, TypeVarType) for t in template.items
        ):
            actual = get_proper_type(actual.upper_bound)

    # Now handle the case of either template or actual being a Union.
    # For a Union to be a subtype of another type, every item of the Union
    # must be a subtype of that type, so concatenate the constraints.
    if direction == SUBTYPE_OF and isinstance(template, UnionType):
        res = []
        for t_item in template.items:
            res.extend(infer_constraints(t_item, actual, direction))
        return res
    if direction == SUPERTYPE_OF and isinstance(actual, UnionType):
        res = []
        for a_item in actual.items:
            # `orig_template` has to be preserved intact in case it's recursive.
            # If we unwrapped ``type[...]`` previously, wrap the item back again,
            # as ``type[...]`` can't be removed from `orig_template`.
            if type_type_unwrapped:
                a_item = TypeType.make_normalized(a_item)
            res.extend(infer_constraints(orig_template, a_item, direction))
        return res

    # Now the potential subtype is known not to be a Union or a type
    # variable that we are solving for. In that case, for a Union to
    # be a supertype of the potential subtype, some item of the Union
    # must be a supertype of it.
    if direction == SUBTYPE_OF and isinstance(actual, UnionType):
        # We infer constraints eagerly -- try to find constraints for a type
        # variable if possible. This seems to help with some real-world
        # use cases.
        return any_constraints(
            [
                infer_constraints_if_possible(template, a_item, direction)
                for a_item in actual.items
            ],
            eager=True,
        )
    if direction == SUPERTYPE_OF and isinstance(template, UnionType):
        # When the template is a union, we are okay with leaving some
        # type variables indeterminate. This helps with some special
        # cases, though this isn't very principled.
        result = any_constraints(
            [
                infer_constraints_if_possible(t_item, actual, direction)
                for t_item in template.items
            ],
            eager=isinstance(actual, AnyType),
        )
        if result:
            return result
        elif has_recursive_types(template) and not has_recursive_types(actual):
            return handle_recursive_union(template, actual, direction)
        return []

    # Remaining cases are handled by ConstraintBuilderVisitor.
    return template.accept(ConstraintBuilderVisitor(actual, direction, skip_neg_op, erase_types))

