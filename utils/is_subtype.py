
def is_subtype(type1, type2) -> bool:
    """Check if *type1* is a subtype of *type2*."""
    return _type_check(type1=type2, type2=type1)


def is_subtype(
    left: Type,
    right: Type,
    *,
    subtype_context: SubtypeContext | None = None,
    ignore_type_params: bool = False,
    ignore_pos_arg_names: bool = False,
    ignore_declared_variance: bool = False,
    always_covariant: bool = False,
    ignore_promotions: bool = False,
    options: Options | None = None,
) -> bool:
    """Is 'left' subtype of 'right'?

    Also consider Any to be a subtype of any type, and vice versa. This
    recursively applies to components of composite types (List[int] is subtype
    of List[Any], for example).

    type_parameter_checker is used to check the type parameters (for example,
    A with B in is_subtype(C[A], C[B]). The default checks for subtype relation
    between the type arguments (e.g., A and B), taking the variance of the
    type var into account.
    """
    if left == right:
        return True
    if subtype_context is None:
        subtype_context = SubtypeContext(
            ignore_type_params=ignore_type_params,
            ignore_pos_arg_names=ignore_pos_arg_names,
            ignore_declared_variance=ignore_declared_variance,
            always_covariant=always_covariant,
            ignore_promotions=ignore_promotions,
            options=options,
        )
    else:
        assert (
            not ignore_type_params
            and not ignore_pos_arg_names
            and not ignore_declared_variance
            and not always_covariant
            and not ignore_promotions
            and options is None
        ), "Don't pass both context and individual flags"
    if type_state.is_assumed_subtype(left, right):
        return True
    if mypy.typeops.is_recursive_pair(left, right):
        # This case requires special care because it may cause infinite recursion.
        # Our view on recursive types is known under a fancy name of iso-recursive mu-types.
        # Roughly this means that a recursive type is defined as an alias where right hand side
        # can refer to the type as a whole, for example:
        #     A = Union[int, Tuple[A, ...]]
        # and an alias unrolled once represents the *same type*, in our case all these represent
        # the same type:
        #    A
        #    Union[int, Tuple[A, ...]]
        #    Union[int, Tuple[Union[int, Tuple[A, ...]], ...]]
        # The algorithm for subtyping is then essentially under the assumption that left <: right,
        # check that get_proper_type(left) <: get_proper_type(right). On the example above,
        # If we start with:
        #     A = Union[int, Tuple[A, ...]]
        #     B = Union[int, Tuple[B, ...]]
        # When checking if A <: B we push pair (A, B) onto 'assuming' stack, then when after few
        # steps we come back to initial call is_subtype(A, B) and immediately return True.
        with pop_on_exit(type_state.get_assumptions(is_proper=False), left, right):
            return _is_subtype(left, right, subtype_context, proper_subtype=False)
    return _is_subtype(left, right, subtype_context, proper_subtype=False)


def is_subtype(left: RType, right: RType, *, relaxed: bool = False) -> bool:
    if is_object_rprimitive(right):
        return True
    elif isinstance(right, RUnion):
        if isinstance(left, RUnion):
            for left_item in left.items:
                if not any(
                    is_subtype(left_item, right_item, relaxed=relaxed)
                    for right_item in right.items
                ):
                    return False
            return True
        else:
            return any(is_subtype(left, item, relaxed=relaxed) for item in right.items)
    return left.accept(SubtypeVisitor(right, relaxed=relaxed))

