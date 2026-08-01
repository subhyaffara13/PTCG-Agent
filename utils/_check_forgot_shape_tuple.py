
def _check_forgot_shape_tuple(name, shape, dtype) -> str | None:
  if isinstance(dtype, int) and isinstance(shape, int):
    return (f"Cannot interpret '{dtype}' as a data type."
            f"\n\nDid you accidentally write "
            f"`jax.numpy.{name}({shape}, {dtype})` "
            f"when you meant `jax.numpy.{name}(({shape}, {dtype}))`, i.e. "
            "with a single tuple argument for the shape?")

