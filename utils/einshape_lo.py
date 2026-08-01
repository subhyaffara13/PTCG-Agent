
def einshape_lo(
    equation: str, x: jax_typing.Array, assert_is_tile_preserving: bool, **sizes: int
) -> jax_typing.Array:
  return einshape_lo_p.bind(
      x,
      equation=equation,
      sizes=tuple(sizes.items()),
      assert_is_tile_preserving=assert_is_tile_preserving,
  )

