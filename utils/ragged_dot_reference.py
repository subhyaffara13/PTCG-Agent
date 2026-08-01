
def ragged_dot_reference(a, b, g):
  return lax.ragged_dot(a, b, g, preferred_element_type=jnp.float16)

