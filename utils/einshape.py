
def einshape(
    equation: str,
    x: jax_typing.Array,
    assert_is_tile_preserving: bool = False,
    **sizes: int,
) -> jax_typing.Array:
  """Reshapes and transposes an array according to an einshape equation.

  Args:
    equation: A string defining the transformation, e.g., "ab(cd)->cabd". -
      Names (e.g., 'a', 'b') represent dimensions. - Parentheses on the LHS,
      like `(cd)`, indicate a dimension that will be split into dimensions `c`
      and `d`. - Parentheses on the RHS, like `(ab)`, indicate dimensions `a`
      and `b` that will be merged.
    x: The input jax_typing.Array to transform.
    assert_is_tile_preserving: If True, assert that the transformation is tile
      preserving. Note that this check only applies inside of Pallas kernels.
    **sizes: Dimension sizes that cannot be inferred from the input shape.
      Required when splitting dimensions unless all but one sub-dimension size
      is known.

  Returns:
    The transformed jax_typing.Array.

  Examples:
    >>> import jax.numpy as jnp
    >>> x = jnp.zeros((10, 20))
    >>> # Split the second dimension (20) into (4, 5)
    >>> y = einshape("a(bc)->abc", x, b=4)
    >>> y.shape
    (10, 4, 5)

    >>> # Transpose and merge the first two dimensions.
    >>> z = einshape("abc->(ba)c", y)
    >>> z.shape
    (40, 5)
  """
  return Einshape(
      jax_core.typeof(x),
      equation=equation,
      sizes=sizes,
      assert_is_tile_preserving=assert_is_tile_preserving,
  )(x)

