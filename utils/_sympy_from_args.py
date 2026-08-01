
def _sympy_from_args(
    cls: type[sympy.Add | sympy.Mul],
    args: list[sympy.Expr],
    sort: bool = True,
    is_commutative: bool | None = None,
) -> sympy.Expr:
    """
    Create a sympy expression from a list of arguments, optimizing for performance.

    This function creates a sympy Add or Mul expression from a list of arguments
    while avoiding expensive operations like flattening. It handles sorting the
    arguments appropriately based on the expression type.

    Args:
        cls: The sympy class to create (Add or Mul)
        args: List of sympy expressions to combine
        sort: Whether to sort the arguments (default: True)
        is_commutative: Whether the operation is commutative (default: None)

    Returns:
        A sympy expression of type cls combining all arguments

    Raises:
        ValueError: If cls is not sympy.Add or sympy.Mul
    """

    if not args:
        return cls.identity  # type: ignore[union-attr]

    # These args are already in canonical form, so we avoid calling
    # Add(*args) to avoid expensive Add.flatten operation
    if sort:
        if cls is sympy.Add:
            sort_fn = sympy.core.add._addsort
        elif cls is sympy.Mul:
            sort_fn = sympy.core.mul._mulsort
        else:
            raise ValueError(f"Unknown cls: {cls}")

        # we don't support non commutative with sort
        if is_commutative is not True:
            raise AssertionError("is_commutative must be True")
        if args[0].is_Number:
            rest = args[1:]
            sort_fn(rest)
            return cls._from_args([args[0]] + rest, is_commutative=is_commutative)  # type: ignore[attr-defined]
        else:
            args = args.copy()
            sort_fn(args)
            return cls._from_args(args, is_commutative=is_commutative)  # type: ignore[attr-defined]
    else:
        # if the args are already sorted, we create directly
        return cls._from_args(args, is_commutative=is_commutative)  # type: ignore[attr-defined]

