
def _is_subdtype(dtype, base) -> bool:
  """Safely checks for dtype subtyping."""
  assert jax is not None
  jnp = jax.numpy
  try:
    return jnp.issubdtype(dtype, base)
  except TypeError:
    return False


def _is_subdtype(dtype, dtypes):
    """
    Shorthand for calculating whether dtype is subtype of some dtypes.

    Also allows specifying a list instead of just a single dtype.

    Additionaly, the most important supertypes from
        https://numpy.org/doc/stable/reference/arrays.scalars.html
    can optionally be specified using abbreviations as follows:
        "i": np.integer
        "f": np.floating
        "c": np.complexfloating
        "n": np.number (contains the other three)
    """
    dtypes = dtypes if isinstance(dtypes, list) else [dtypes]
    # map single character abbreviations, if they are in dtypes
    mapping = {
        "i": np.integer,
        "f": np.floating,
        "c": np.complexfloating,
        "n": np.number
    }
    dtypes = [mapping.get(x, x) for x in dtypes]
    return any(np.issubdtype(dtype, dt) for dt in dtypes)

