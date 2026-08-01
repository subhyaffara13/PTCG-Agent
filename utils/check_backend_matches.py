
def check_backend_matches(inner_backend: str | None,
                          lowering_platforms: Sequence[str]):
  # For nested calls, the outermost call sets the backend for all inner calls;
  # it's an error if the inner call has a conflicting explicit backend spec.
  if inner_backend is None:
    return
  outer_backend, *more_lowering_platforms = lowering_platforms
  if more_lowering_platforms:
    raise NotImplementedError(
        "Multi-platform lowering when a backend= parameter is specified")
  if (inner_backend != outer_backend and
      outer_backend not in xb.expand_platform_alias(inner_backend)):
    raise ValueError(
        f"Outer-jit backend specification {outer_backend} must match explicit "
        f"inner-jit backend specification {inner_backend}.")

