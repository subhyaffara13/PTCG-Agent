
def _lift(accumulator: Accumulator) -> Accumulator:
  """Lifts an array-based Accumulator to a PyTree-based Accumulator."""
  return Accumulator(
      lambda value: jax.tree.map(accumulator.init, value),
      lambda carry, value, i: jax.tree.map(
          lambda c, v: accumulator.update(c, v, i), carry, value
      ),
      lambda carry: jax.tree.map(accumulator.finalize, carry),
      lambda values: jax.tree.map(accumulator.aggregate, values),
  )

