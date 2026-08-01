
def program_id(axis: int) -> jax_typing.Array:
  """Returns the kernel execution position along the given axis of the grid.

  For example, with a 2D ``grid`` in the kernel execution corresponding to the
  grid coordinates ``(1, 2)``,
  ``program_id(axis=0)`` returns ``1`` and ``program_id(axis=1)`` returns ``2``.

  The returned value is an array of shape ``()`` and dtype ``int32``.

  Args:
    axis: the axis of the grid along which to count the program.
  """
  return program_id_p.bind(axis=axis)

