
def is_overlapping_types(
    left: Type,
    right: Type,
    ignore_promotions: bool = False,
    overlap_for_overloads: bool = False,
    seen_types: set[tuple[Type, Type]] | None = None,
) -> bool:
    """Can a value of type 'left' also be of type 'right' or vice-versa?

    If 'ignore_promotions' is True, we ignore promotions while checking for overlaps.
    If 'overlap_for_overloads' is True, we check for overlaps more strictly (to avoid false
    positives), for example: None only overlaps with explicitly optional types, Any
    doesn't overlap with anything except object, we don't ignore positional argument names.
    """
    if isinstance(left, TypeGuardedType) or isinstance(right, TypeGuardedType):
        # A type guard forces the new type even if it doesn't overlap the old.
        return True

    if seen_types is None:
        seen_types = set()
    elif (left, right) in seen_types:
        return True
    if is_recursive_pair(left, right):
        seen_types.add((left, right))

    left, right = get_proper_types((left, right))

    # We should never encounter this type.
    if isinstance(left, PartialType) or isinstance(right, PartialType):
        assert False, "Unexpectedly encountered partial type"

    # We should also never encounter these types, but it's possible a few
    # have snuck through due to unrelated bugs. For now, we handle these
    # in the same way we handle 'Any'.
    #
    # TODO: Replace these with an 'assert False' once we are more confident.
    illegal_types = (UnboundType, ErasedType, DeletedType)
    if isinstance(left, illegal_types) or isinstance(right, illegal_types):
        return True

    # When running under non-strict optional mode, simplify away types of
    # the form 'Union[A, B, C, None]' into just 'Union[A, B, C]'.

    if not state.strict_optional:
        if isinstance(left, UnionType):
            left = UnionType.make_union(left.relevant_items())
        if isinstance(right, UnionType):
            right = UnionType.make_union(right.relevant_items())
        left, right = get_proper_types((left, right))

    # 'Any' may or may not be overlapping with the other type
    if isinstance(left, AnyType) or isinstance(right, AnyType):
        return not overlap_for_overloads or is_object(left) or is_object(right)

    # We check for complete overlaps next as a general-purpose failsafe.
    # If this check fails, we start checking to see if there exists a
    # *partial* overlap between types.
    #
    # These checks will also handle the NoneType and UninhabitedType cases for us.

    # enums are sometimes expanded into an Union of Literals
    # when that happens we want to make sure we treat the two as overlapping
    # and crucially, we want to do that *fast* in case the enum is large
    # so we do it before expanding variants below to avoid O(n**2) behavior
    if (
        is_enum_overlapping_union(left, right)
        or is_enum_overlapping_union(right, left)
        or is_literal_in_union(left, right)
        or is_literal_in_union(right, left)
    ):
        return True

    if overlap_for_overloads:
        if is_none_object_overlap(left, right) or is_none_object_overlap(right, left):
            return False

    if are_related_types(
        left, right, proper_subtype=overlap_for_overloads, ignore_promotions=ignore_promotions
    ):
        return True

    # See the docstring for 'get_possible_variants' for more info on what the
    # following lines are doing.

    left_possible = get_possible_variants(left)
    right_possible = get_possible_variants(right)

    # Now move on to checking multi-variant types like Unions. We also perform
    # the same logic if either type happens to be a TypeVar/ParamSpec/TypeVarTuple.
    #
    # Handling the TypeVarLikes now lets us simulate having them bind to the corresponding
    # type -- if we deferred these checks, the "return-early" logic of the other
    # checks will prevent us from detecting certain overlaps.
    #
    # If both types are singleton variants (and are not TypeVarLikes), we've hit the base case:
    # we skip these checks to avoid infinitely recursing.

    def _is_overlapping_types(left: Type, right: Type) -> bool:
        """Encode the kind of overlapping check to perform.

        This function mostly exists, so we don't have to repeat keyword arguments everywhere.
        """
        return is_overlapping_types(
            left,
            right,
            ignore_promotions=ignore_promotions,
            overlap_for_overloads=overlap_for_overloads,
            seen_types=seen_types.copy(),
        )

    if (
        len(left_possible) > 1
        or len(right_possible) > 1
        or isinstance(left, TypeVarLikeType)
        or isinstance(right, TypeVarLikeType)
    ):
        for l in left_possible:
            for r in right_possible:
                if _is_overlapping_types(l, r):
                    return True
        return False

    # Now that we've finished handling TypeVarLikes, we're free to end early
    # if one one of the types is None and we're running in strict-optional mode.
    # (None only overlaps with None in strict-optional mode).
    #
    # We must perform this check after the TypeVarLike checks because
    # a TypeVar could be bound to None, for example.

    if state.strict_optional and isinstance(left, NoneType) != isinstance(right, NoneType):
        return False

    # Next, we handle single-variant types that may be inherently partially overlapping:
    #
    # - TypedDicts
    # - Tuples
    #
    # If we cannot identify a partial overlap and end early, we degrade these two types
    # into their 'Instance' fallbacks.

    if isinstance(left, TypedDictType) and isinstance(right, TypedDictType):
        return are_typed_dicts_overlapping(left, right, _is_overlapping_types)
    elif typed_dict_mapping_pair(left, right):
        # Overlaps between TypedDicts and Mappings require dedicated logic.
        return typed_dict_mapping_overlap(left, right, overlapping=_is_overlapping_types)
    elif isinstance(left, TypedDictType):
        left = left.fallback
    elif isinstance(right, TypedDictType):
        right = right.fallback

    if is_tuple(left) and is_tuple(right):
        return are_tuples_overlapping(left, right, _is_overlapping_types)
    elif isinstance(left, TupleType):
        left = tuple_fallback(left)
    elif isinstance(right, TupleType):
        right = tuple_fallback(right)

    # Next, we handle single-variant types that cannot be inherently partially overlapping,
    # but do require custom logic to inspect.
    #
    # As before, we degrade into 'Instance' whenever possible.

    if isinstance(left, TypeType) and isinstance(right, TypeType):
        return _is_overlapping_types(left.item, right.item)

    if isinstance(left, TypeType) or isinstance(right, TypeType):

        def _type_object_overlap(left: Type, right: Type) -> bool:
            """Special cases for type object types overlaps."""
            # TODO: these checks are a bit in gray area, adjust if they cause problems.
            left, right = get_proper_types((left, right))
            # 1. Type[C] vs Callable[..., C] overlap even if the latter is not class object.
            if isinstance(left, TypeType) and isinstance(right, CallableType):
                return _is_overlapping_types(left.item, right.ret_type)
            # 2. Type[C] vs Meta, where Meta is a metaclass for C.
            if isinstance(left, TypeType) and isinstance(right, Instance):
                if isinstance(left.item, Instance):
                    left_meta = left.item.type.metaclass_type
                    if left_meta is not None:
                        return _is_overlapping_types(left_meta, right)
                    # builtins.type (default metaclass) overlaps with all metaclasses
                    return right.type.has_base("builtins.type")
                elif isinstance(left.item, AnyType):
                    return right.type.has_base("builtins.type")
            # 3. Callable[..., C] vs Meta is considered below, when we switch to fallbacks.
            return False

        return _type_object_overlap(left, right) or _type_object_overlap(right, left)

    if isinstance(left, Parameters) and isinstance(right, Parameters):
        return are_parameters_compatible(
            left,
            right,
            is_compat=_is_overlapping_types,
            is_proper_subtype=False,
            ignore_pos_arg_names=not overlap_for_overloads,
            allow_partial_overlap=True,
        )
    # A `Parameters` does not overlap with anything else, however
    if isinstance(left, Parameters) or isinstance(right, Parameters):
        return False

    if isinstance(left, CallableType) and isinstance(right, CallableType):
        # We run is_callable_compatible in both directions, similar to the logic
        # in is_unsafe_overlapping_overload_signatures
        # See comments in https://github.com/python/mypy/pull/5476
        return is_callable_compatible(
            left,
            right,
            is_compat=_is_overlapping_types,
            is_proper_subtype=False,
            ignore_pos_arg_names=not overlap_for_overloads,
            allow_partial_overlap=True,
        ) or is_callable_compatible(
            right,
            left,
            is_compat=_is_overlapping_types,
            is_proper_subtype=False,
            ignore_pos_arg_names=not overlap_for_overloads,
            check_args_covariantly=True,
            allow_partial_overlap=True,
        )

    call = None
    other = None
    if isinstance(left, CallableType) and isinstance(right, Instance):
        call = find_member("__call__", right, right, is_operator=True)
        other = left
    if isinstance(right, CallableType) and isinstance(left, Instance):
        call = find_member("__call__", left, left, is_operator=True)
        other = right
    if isinstance(get_proper_type(call), FunctionLike):
        assert call is not None and other is not None
        return _is_overlapping_types(call, other)

    if isinstance(left, CallableType):
        left = left.fallback
    if isinstance(right, CallableType):
        right = right.fallback

    if isinstance(left, LiteralType) and isinstance(right, LiteralType):
        if left.value == right.value:
            # If values are the same, we still need to check if fallbacks are overlapping,
            # this is done below.
            left = left.fallback
            right = right.fallback
        else:
            return False
    elif isinstance(left, LiteralType):
        left = left.fallback
    elif isinstance(right, LiteralType):
        right = right.fallback

    # Finally, we handle the case where left and right are instances.

    if isinstance(left, Instance) and isinstance(right, Instance):
        # First we need to handle promotions and structural compatibility for instances
        # that came as fallbacks, so simply call is_subtype() to avoid code duplication.
        if are_related_types(
            left, right, proper_subtype=overlap_for_overloads, ignore_promotions=ignore_promotions
        ):
            return True

        if right.type.fullname == "builtins.int" and left.type.fullname in MYPYC_NATIVE_INT_NAMES:
            return True

        # Two unrelated types cannot be partially overlapping: they're disjoint.
        if left.type.has_base(right.type.fullname):
            left = map_instance_to_supertype(left, right.type)
        elif right.type.has_base(left.type.fullname):
            right = map_instance_to_supertype(right, left.type)
        else:
            return False

        if right.type.has_type_var_tuple_type:
            # Similar to subtyping, we delegate the heavy lifting to the tuple overlap.
            assert right.type.type_var_tuple_prefix is not None
            assert right.type.type_var_tuple_suffix is not None
            prefix = right.type.type_var_tuple_prefix
            suffix = right.type.type_var_tuple_suffix
            tvt = right.type.defn.type_vars[prefix]
            assert isinstance(tvt, TypeVarTupleType)
            fallback = tvt.tuple_fallback
            left_prefix, left_middle, left_suffix = split_with_prefix_and_suffix(
                left.args, prefix, suffix
            )
            right_prefix, right_middle, right_suffix = split_with_prefix_and_suffix(
                right.args, prefix, suffix
            )
            left_args = left_prefix + (TupleType(list(left_middle), fallback),) + left_suffix
            right_args = right_prefix + (TupleType(list(right_middle), fallback),) + right_suffix
        else:
            left_args = left.args
            right_args = right.args
        if len(left_args) == len(right_args):
            # Note: we don't really care about variance here, since the overlapping check
            # is symmetric and since we want to return 'True' even for partial overlaps.
            #
            # For example, suppose we have two types Wrapper[Parent] and Wrapper[Child].
            # It doesn't matter whether Wrapper is covariant or contravariant since
            # either way, one of the two types will overlap with the other.
            #
            # Similarly, if Wrapper was invariant, the two types could still be partially
            # overlapping -- what if Wrapper[Parent] happened to contain only instances of
            # specifically Child?
            #
            # Or, to use a more concrete example, List[Union[A, B]] and List[Union[B, C]]
            # would be considered partially overlapping since it's possible for both lists
            # to contain only instances of B at runtime.
            if all(
                _is_overlapping_types(left_arg, right_arg)
                for left_arg, right_arg in zip(left_args, right_args)
            ):
                return True

        return False

    # We ought to have handled every case by now: we conclude the
    # two types are not overlapping, either completely or partially.
    #
    # Note: it's unclear however, whether returning False is the right thing
    # to do when inferring reachability -- see  https://github.com/python/mypy/issues/5529

    assert type(left) != type(right), f"{type(left)} vs {type(right)}"
    return False

