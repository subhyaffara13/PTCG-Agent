
def touch(filename: str) -> None:
    with open(filename, "a"):
        pass


def touch(filename):
    open(filename, 'wb').close()


def touch(path):
    open(path, 'wb').close()
    return path


def touch(ref: jax.Array | state.TransformedRef) -> None:
  """Adds a fake read-write dependency to the given ref."""
  ref_leaves = jax.tree.leaves(ref)
  ref_leaves = [ref.ref if isinstance(ref, state.TransformedRef) else ref
                for ref in ref_leaves]
  for ref in ref_leaves:
    touch_p.bind(ref)

