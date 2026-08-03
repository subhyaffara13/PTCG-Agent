from typing import Any

def tree_unflatten(leaves: Iterable[Any], treespec: TreeSpec) -> PyTree:
    """Reconstruct a pytree from the treespec and the leaves.

    The inverse of :func:`tree_flatten`.

    >>> tree = {"b": (2, [3, 4]), "a": 1, "c": None, "d": 5}
    >>> leaves, treespec = tree_flatten(tree)
    >>> tree == tree_unflatten(leaves, treespec)
    True

    Args:
        leaves (iterable): The list of leaves to use for reconstruction. The list must match the
            number of leaves of the treespec.
        treespec (TreeSpec): The treespec to reconstruct.

    Returns:
        The reconstructed pytree, containing the ``leaves`` placed in the structure described by
        ``treespec``.
    """
    if not _is_pytreespec_instance(treespec):
        if not _is_pytreespec_instance(leaves):
            raise TypeError(
                f"Expected `treespec` to be an instance of "
                f"PyTreeSpec but got item of type {type(treespec)}."
            )
        # Allow passing the PyTreeSpec instance as the first argument
        # pyrefly: ignore [bad-assignment]
        leaves, treespec = treespec, leaves
    return treespec.unflatten(leaves)


def tree_unflatten(leaves: Iterable[Any], treespec: TreeSpec) -> PyTree:
    """Given a list of values and a TreeSpec, builds a pytree.
    This is the inverse operation of `tree_flatten`.
    """
    if not _is_pytreespec_instance(treespec):
        if not _is_pytreespec_instance(leaves):
            raise TypeError(
                f"Expected `treespec` to be an instance of "
                f"PyTreeSpec but got item of type {type(treespec)}."
            )
        # Allow passing the PyTreeSpec instance as the first argument
        leaves, treespec = treespec, leaves
    return treespec.unflatten(leaves)


def tree_unflatten(treespec: PyTreeSpec, leaves: Iterable[Any]) -> PyTree:
    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"Expected `treespec` to be an instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )
    return treespec.unflatten(leaves)


def tree_unflatten(treedef: PyTreeDef, leaves: Iterable[Leaf]) -> Any:
  """Alias of :func:`jax.tree.unflatten`."""
  return treedef.unflatten(leaves)

