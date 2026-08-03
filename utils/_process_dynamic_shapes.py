from typing import Any

def _process_dynamic_shapes(
    combined_args: dict[str, Any],
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any] | None,
) -> list[Constraint]:
    """
    Reads the dynamic_shapes specification and produces a list of constraints.
    """
    from torch._dynamo.exc import UserError, UserErrorType

    if dynamic_shapes is None or len(dynamic_shapes) == 0:
        # we run with dynamic by default, so no need to produce constraints
        return []
    if isinstance(dynamic_shapes, (tuple, list)):
        combined_args = type(dynamic_shapes)(combined_args.values())  # type: ignore[assignment, misc]

    # map of Dim names representing input shape dimensions to constraints on them
    symbols: dict[str, list[Constraint]] = defaultdict(list)
    # track roots that do not directly represent input shape dimensions
    phantom_roots: dict[str, _PhantomRoot] = {}
    derived_constraints_with_phantom_root: list[_DerivedConstraint] = []
    # list of constraints to return
    constraints: list[Constraint] = []

    def to_constraint(dim, tensor, i):
        import sympy

        from torch.fx.experimental.symbolic_shapes import StrictMinMaxConstraint
        from torch.utils._sympy.solve import try_solve
        from torch.utils._sympy.value_ranges import ValueRanges

        def root_value():
            # given tensor.shape[i] is the value of dim = fn(root),
            # find the value of root
            symbol = sympy.Symbol(dim.root.__name__, integer=True)
            expr = dim.fn(symbol)
            solution = try_solve(sympy.Eq(expr, tensor.shape[i]), symbol)
            if solution is not None:
                return int(solution[1])
            else:
                raise UserError(  # noqa: B904
                    UserErrorType.CONSTRAINT_VIOLATION,
                    f"Expected shape[{i}] = {tensor.shape[i]} of input Tensor to be "
                    f"of the form {expr}, where {symbol} is an integer",
                )

        if isinstance(dim, _DerivedDim):
            # generate a _DerivedConstraint where the root is:
            # - either a _ConstraintTarget (if dim.root directly describes an input shape)
            # - or a _PhantomRoot (otherwise)
            dim_root = dim.root  # type: ignore[attr-defined]
            if dim_root.__name__ in symbols:
                # root represents an input shape dimension
                root_constraint = symbols[dim_root.__name__][0]
                root = _ConstraintTarget(
                    root_constraint.t_id,
                    root_constraint.dim,
                )
            elif dim_root.__name__ not in phantom_roots:
                # create a phantom root
                root = _PhantomRoot(  # type: ignore[assignment]
                    name=dim_root.__name__,
                    constraint_range=StrictMinMaxConstraint(
                        vr=ValueRanges(lower=dim_root.min, upper=dim_root.max),
                        warn_only=False,
                    ),
                    val=root_value(),
                )
                phantom_roots[dim_root.__name__] = root  # type: ignore[assignment]
            else:
                root = phantom_roots[dim_root.__name__]  # type: ignore[assignment]
            constraint = _DerivedConstraint(
                id(tensor),
                i,
                dim.__name__,
                StrictMinMaxConstraint(
                    vr=ValueRanges(lower=dim.min, upper=dim.max),
                    warn_only=False,
                ),
                root,
                dim.fn,  # type: ignore[attr-defined]
            )
            if isinstance(root, _PhantomRoot):
                # NOTE(avik): since we have not processed all inputs yet, we may replace this
                # with a root that does represent an input shape dimension later (see below)
                derived_constraints_with_phantom_root.append(constraint)
        elif isinstance(dim, _StaticDim):
            constraint = _Constraint(  # type: ignore[assignment]
                id(tensor),
                i,
                dim.__name__,
                StrictMinMaxConstraint(
                    vr=ValueRanges(lower=dim.value, upper=dim.value),  # type: ignore[attr-defined]
                    warn_only=False,
                ),
            )
        else:
            if not isinstance(dim, Dim):
                raise AssertionError(f"expected dim to be Dim, got {type(dim)}")
            constraint = _Constraint(  # type: ignore[assignment]
                id(tensor),
                i,
                dim.__name__,
                StrictMinMaxConstraint(
                    vr=ValueRanges(lower=dim.min, upper=dim.max),  # type: ignore[attr-defined]
                    warn_only=False,
                ),
            )
        return constraint

    def _parse_tensor_dim(tensor, idx, dim) -> None:
        def _create_static_dim(tensor, i, value):
            return _StaticDim(value)

        if isinstance(dim, (int, Dim)):
            if isinstance(dim, int):
                dim = _create_static_dim(tensor, idx, dim)
            constraint = to_constraint(dim, tensor, idx)
            symbols[dim.__name__].append(constraint)
        elif isinstance(dim, _DimHint):
            if dim.type == _DimHintType.AUTO:
                torch._dynamo.maybe_mark_dynamic(tensor, idx)
            elif dim.type == _DimHintType.STATIC:
                torch._dynamo.mark_static(tensor, idx)
            elif dim.type == _DimHintType.DYNAMIC:
                torch._dynamo.mark_dynamic(tensor, idx)
            constraints.append(_RelaxedConstraint(id(tensor), idx))
        elif dim is None:
            torch._dynamo.mark_static(tensor, idx)

    def update_symbols(path, tensor, shape):
        # clean out decorators from user side, or previous export call
        # we also delete these attributes in non_strict_utils.py/make_constraints()
        tensor._dynamo_weak_dynamic_indices = set()
        tensor._dynamo_dynamic_indices = set()
        tensor._dynamo_dynamic_range = set()
        tensor._dynamo_static_indices = set()
        tensor._dynamo_unbacked_indices = set()

        if isinstance(shape, dict):
            for i, dim in shape.items():
                _parse_tensor_dim(tensor, i, dim)
        elif isinstance(shape, (tuple, list)):
            for i, dim in enumerate(shape):
                _parse_tensor_dim(tensor, i, dim)
        elif shape is None:
            for i in range(tensor.dim()):
                _parse_tensor_dim(tensor, i, None)

    def assoc_shape(path, t, dynamic_shape):
        if isinstance(t, torch.Tensor):
            update_symbols(path, t, dynamic_shape)
        elif isinstance(t, _IntWrapper):
            # If tensor dimensions are marked as dynamic, the tensors themselves
            # get marked using mark_dynamic. However since we can't mark
            # integers as dynamic, we first wrap integers in this class, and
            # then set the `dim` field of the class with the dynamic shapes dim
            # to mark the integer as dynamic.
            t.dynamism = dynamic_shape

    _tree_map_with_path(assoc_shape, combined_args, dynamic_shapes, tree_name="inputs")

    for derived_constraint_with_phantom_root in derived_constraints_with_phantom_root:
        phantom_root_name = derived_constraint_with_phantom_root.root.name  # type: ignore[union-attr]
        if phantom_root_name in symbols:
            # We found an input shape dimension corresponding to this name, so we
            # do not need a phantom symbol for it after all.
            # NOTE(avik): Overall we want to maintain the invariant that roots that
            # are phantom symbols are really "phantom," i.e., they cannot be represented
            # by any input source. This is important when we are deciding derived equalities,
            # since we can focus our attention exclusively on input sources: deciding
            # derived equalities involving phantom symbols are, in comparison, trivial.
            derived_constraint_with_phantom_root.root = symbols[phantom_root_name][0]

    for dynamic_dims in symbols.values():
        constraints.extend(dynamic_dims)

    return constraints

