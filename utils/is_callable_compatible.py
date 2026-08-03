from typing import Callable

def is_callable_compatible(
    left: CallableType,
    right: CallableType,
    *,
    is_compat: Callable[[Type, Type], bool],
    is_proper_subtype: bool,
    is_compat_return: Callable[[Type, Type], bool] | None = None,
    ignore_return: bool = False,
    ignore_pos_arg_names: bool = False,
    check_args_covariantly: bool = False,
    allow_partial_overlap: bool = False,
    strict_concatenate: bool = False,
) -> bool:
    """Is the left compatible with the right, using the provided compatibility check?

    is_compat:
        The check we want to run against the parameters.

    is_compat_return:
        The check we want to run against the return type.
        If None, use the 'is_compat' check.

    check_args_covariantly:
        If true, check if the left's args is compatible with the right's
        instead of the other way around (contravariantly).

        This function is mostly used to check if the left is a subtype of the right which
        is why the default is to check the args contravariantly. However, it's occasionally
        useful to check the args using some other check, so we leave the variance
        configurable.

        For example, when checking the validity of overloads, it's useful to see if
        the first overload alternative has more precise arguments than the second.
        We would want to check the arguments covariantly in that case.

        Note! The following two function calls are NOT equivalent:

            is_callable_compatible(f, g, is_compat=is_subtype, check_args_covariantly=False)
            is_callable_compatible(g, f, is_compat=is_subtype, check_args_covariantly=True)

        The two calls are similar in that they both check the function arguments in
        the same direction: they both run `is_subtype(argument_from_g, argument_from_f)`.

        However, the two calls differ in which direction they check things like
        keyword arguments. For example, suppose f and g are defined like so:

            def f(x: int, *y: int) -> int: ...
            def g(x: int) -> int: ...

        In this case, the first call will succeed and the second will fail: f is a
        valid stand-in for g but not vice-versa.

    allow_partial_overlap:
        By default this function returns True if and only if *all* calls to left are
        also calls to right (with respect to the provided 'is_compat' function).

        If this parameter is set to 'True', we return True if *there exists at least one*
        call to left that's also a call to right.

        In other words, we perform an existential check instead of a universal one;
        we require left to only overlap with right instead of being a subset.

        For example, suppose we set 'is_compat' to some subtype check and compare following:

            f(x: float, y: str = "...", *args: bool) -> str
            g(*args: int) -> str

        This function would normally return 'False': f is not a subtype of g.
        However, we would return True if this parameter is set to 'True': the two
        calls are compatible if the user runs "f_or_g(3)". In the context of that
        specific call, the two functions effectively have signatures of:

            f2(float) -> str
            g2(int) -> str

        Here, f2 is a valid subtype of g2 so we return True.

        Specifically, if this parameter is set this function will:

        -   Ignore optional arguments on either the left or right that have no
            corresponding match.
        -   No longer mandate optional arguments on either side are also optional
            on the other.
        -   No longer mandate that if right has a *arg or **kwarg that left must also
            have the same.

        Note: when this argument is set to True, this function becomes "symmetric" --
        the following calls are equivalent:

            is_callable_compatible(f, g,
                                   is_compat=some_check,
                                   check_args_covariantly=False,
                                   allow_partial_overlap=True)
            is_callable_compatible(g, f,
                                   is_compat=some_check,
                                   check_args_covariantly=True,
                                   allow_partial_overlap=True)

        If the 'some_check' function is also symmetric, the two calls would be equivalent
        whether or not we check the args covariantly.
    """
    # Normalize both types before comparing them.
    left = left.with_unpacked_kwargs().with_normalized_var_args()
    right = right.with_unpacked_kwargs().with_normalized_var_args()

    if is_compat_return is None:
        is_compat_return = is_compat

    # If either function is implicitly typed, ignore positional arg names too
    if left.implicit or right.implicit:
        ignore_pos_arg_names = True

    # Non-type cannot be a subtype of type.
    if right.is_type_obj() and not left.is_type_obj() and not allow_partial_overlap:
        return False

    # A callable L is a subtype of a generic callable R if L is a
    # subtype of every type obtained from R by substituting types for
    # the variables of R. We can check this by simply leaving the
    # generic variables of R as type variables, effectively varying
    # over all possible values.

    # It's okay even if these variables share ids with generic
    # type variables of L, because generating and solving
    # constraints for the variables of L to make L a subtype of R
    # (below) treats type variables on the two sides as independent.
    if left.variables:
        # Apply generic type variables away in left via type inference.
        unified = unify_generic_callable(left, right, ignore_return=ignore_return)
        if unified is None:
            return False
        left = unified

    # Check return types.
    if not ignore_return and not is_compat_return(left.ret_type, right.ret_type):
        return False

    if check_args_covariantly:
        is_compat = flip_compat_check(is_compat)

    if not strict_concatenate and (left.from_concatenate or right.from_concatenate):
        strict_concatenate_check = False
    else:
        strict_concatenate_check = True

    return are_parameters_compatible(
        left,
        right,
        is_compat=is_compat,
        is_proper_subtype=is_proper_subtype,
        ignore_pos_arg_names=ignore_pos_arg_names,
        allow_partial_overlap=allow_partial_overlap,
        strict_concatenate_check=strict_concatenate_check,
    )

