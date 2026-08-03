from typing import Optional

def restrict_backends(
    *,
    allowed: Optional[Sequence[str]] = None,
    forbidden: Optional[Sequence[str]] = None):
  """Disallows JAX compilation for certain backends.

  Args:
    allowed: Names of backend platforms (e.g. 'cpu' or 'tpu') for which
      compilation is still to be permitted.
    forbidden: Names of backend platforms for which compilation is to be
      forbidden.

  Yields:
    None, in a context where compilation for forbidden platforms will raise
    a `RestrictedBackendError`.

  Raises:
    ValueError: if neither `allowed` nor `forbidden` is specified (i.e. they
      are both `None`), or if anything is both allowed and forbidden.
  """
  allowed = tuple(allowed) if allowed is not None else None
  forbidden = tuple(forbidden) if forbidden is not None else None

  if allowed is None and forbidden is None:
    raise ValueError('No restrictions specified.')
  contradictions = set(allowed or ()) & set(forbidden or ())
  if contradictions:
    raise ValueError(
        f"Backends {contradictions} can't be both allowed and forbidden.")

  def is_allowed(backend_platform):
    return (
        (backend_platform in allowed)
        if allowed is not None
        else (backend_platform not in forbidden)
    )

  with contextlib.ExitStack() as stack:
    # This is for compatibility with JAX both before and after
    # https://github.com/jax-ml/jax/commit/06448864abd6e8187e5b4d9b1ff08ab14fe3b8e0
    if hasattr(compiler, 'backend_compile_and_load'):
      stack.enter_context(
          _restrict_by_attr_name('backend_compile_and_load', is_allowed))
    elif hasattr(compiler, 'backend_compile'):
      stack.enter_context(_restrict_by_attr_name('backend_compile', is_allowed))
    yield

