
def evaluate_shape(shape: Shape, dim_vars: Sequence[str],
                   *dim_values: Array) -> Sequence[Array]:
  """Evaluates a shape possibly containing non-constants.

  Args:
    shape: the shape to evaluate.
    dim_vars: the dimension variables names that may appear in `shape`.
    dim_values: the dimension values corresponding to `dim_vars`.

  Returns:
     a tuple of JAX values corresponding to `shape`, of type
     `dim_value_dtype`.
  """
  env = dict(zip(dim_vars, dim_values))
  def eval_one_dim(d: DimSize):
    try:
      return operator.index(d)
    except:
      # Is a _DimExpr
      return d._evaluate(env)  # pyrefly: ignore[missing-attribute]
  return tuple(eval_one_dim(d) for d in shape)

