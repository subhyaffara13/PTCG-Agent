
def symbolic_shape(shape_spec: str | None,
                   *,
                   constraints: Sequence[str] = (),
                   scope: SymbolicScope | None = None,
                   like: Sequence[int | None] | None = None
                   ) -> Sequence[DimSize]:
  """Constructs a symbolic shape from a string representation.

  See https://docs.jax.dev/en/latest/export/shape_poly.html for examples.

  Args:
    shape_spec: a symbolic shape specification. None stands for "...".
      A shape specification is the string representation of a tuple (the
      parentheses are optional) with comma-separated dimension expressions.
      A dimension expression can be either: an integer constant,
      a dimension variable (alphanumeric
      starting with a letter), e1 + e2, e1 - e2, e1 * e2, floordiv(e1, e2),
      mod(e1, e2), max(e1, e2), or min(e1, e2).
    constraints: a sequence of constraints on symbolic dimension expressions, of
      the form `e1 >= e2` or `e1 <= e2`, or `e1 == e2`.
      See [the documentation](https://docs.jax.dev/en/latest/export/shape_poly.html#user-specified-symbolic-constraints)
      for usage.
    scope: optionally, you can specify that the parsed symbolic expressions
      be created in the given scope. If this is missing, then a new
      `SymbolicScope` is created with the given `constraints`.
      You cannot specify both a `scope` and `constraints` (cannot add new
      constraints to a `scope`).
      See [the documentation](https://docs.jax.dev/en/latest/export/shape_poly.html#user-specified-symbolic-constraints)
      for usage.
    like: when `shape_spec` contains placeholders ("_", "..."), use this
      shape to fill in the placeholders.
      The dimensions of `like` that are used for filling
      must be not `None`. If a dimension in `like` is not `None` and
      the corresponding dimension in `shape_spec` is a constant then they
      must be equal.

  Returns: a tuple with integers or symbolic expressions involving dimension variables.
  """
  shape_spec_repr = repr(shape_spec)
  if shape_spec is None:
    shape_spec = "..."
  elif isinstance(shape_spec, PolyShape):  # TODO: deprecate
    shape_spec = str(shape_spec)
  elif not isinstance(shape_spec, str):
    raise ValueError("polymorphic shape spec should be None or a string. "
                     f"Found {shape_spec_repr}.")
  if scope is None:
    scope = SymbolicScope(constraints)
  elif constraints:
    raise ValueError("Cannot specify both a `scope` and `constraints`.")
  dimensions = _Parser(shape_spec, like, shape_spec_repr, scope).parse()
  return dimensions

