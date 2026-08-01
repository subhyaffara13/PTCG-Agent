
def _remove_noop_transforms(transforms: tuple[Any, ...]) -> tuple[Any, ...]:
  # TODO(jburnim): Instead of just filtering out these transforms, should we
  # check that every access of a buffer uses untiling and/or unswizzling
  # transforms that match how the buffer was allocated?
  return tuple(itertools.dropwhile(lambda t: isinstance(t, NOOP_TRANSFORMS),
                                   transforms))

