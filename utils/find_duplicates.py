
def find_duplicates(a, key=None, ignoremask=True, return_index=False):
    """
    Find the duplicates in a structured array along a given key

    Parameters
    ----------
    a : array-like
        Input array
    key : {string, None}, optional
        Name of the fields along which to check the duplicates.
        If None, the search is performed by records
    ignoremask : {True, False}, optional
        Whether masked data should be discarded or considered as duplicates.
    return_index : {False, True}, optional
        Whether to return the indices of the duplicated values.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.lib import recfunctions as rfn
    >>> ndtype = [('a', int)]
    >>> a = np.ma.array([1, 1, 1, 2, 2, 3, 3],
    ...         mask=[0, 0, 1, 0, 0, 0, 1]).view(ndtype)
    >>> rfn.find_duplicates(a, ignoremask=True, return_index=True)
    (masked_array(data=[(1,), (1,), (2,), (2,)],
                 mask=[(False,), (False,), (False,), (False,)],
           fill_value=(999999,),
                dtype=[('a', '<i8')]), array([0, 1, 3, 4]))
    """
    a = np.asanyarray(a).ravel()
    # Get a dictionary of fields
    fields = get_fieldstructure(a.dtype)
    # Get the sorting data (by selecting the corresponding field)
    base = a
    if key:
        for f in fields[key]:
            base = base[f]
        base = base[key]
    # Get the sorting indices and the sorted data
    sortidx = base.argsort()
    sortedbase = base[sortidx]
    sorteddata = sortedbase.filled()
    # Compare the sorting data
    flag = (sorteddata[:-1] == sorteddata[1:])
    # If masked data must be ignored, set the flag to false where needed
    if ignoremask:
        sortedmask = sortedbase.recordmask
        flag[sortedmask[1:]] = False
    flag = np.concatenate(([False], flag))
    # We need to take the point on the left as well (else we're missing it)
    flag[:-1] = flag[:-1] + flag[1:]
    duplicates = a[sortidx][flag]
    if return_index:
        return (duplicates, sortidx[flag])
    else:
        return duplicates


def find_duplicates(node: tp.Any, /, *, only: filterlib.Filter = ...) -> list[list[PathParts]]:
  """Finds duplicate nodes or node leaves in the given node.

  This function traverses the graph node and collects paths to nodes and leaves
  that have the same identity. It returns a list of lists, where each inner list
  contains paths to nodes or leaves that are duplicates.

  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ...
    >>> class SharedVariables(nnx.Module):
    ...   def __init__(self):
    ...     self.a = nnx.Param(jnp.array(1.0))
    ...     self.b = nnx.Param(jnp.array(2.0))
    ...     self.c = self.b  # shared Variable
    ...
    >>> model = SharedVariables()
    >>> duplicates = nnx.find_duplicates(model)
    >>> len(duplicates)
    1
    >>> for path in duplicates[0]:
    ...   print(path)
    ('b',)
    ('c',)

  ``find_duplicates`` will also find duplicates nodes such as Modules that are
  referenced multiple times in the graph::

    >>> class SharedModules(nnx.Module):
    ...   def __init__(self, rngs: nnx.Rngs):
    ...     self.a = nnx.Linear(1, 1, rngs=rngs)
    ...     self.b = nnx.Linear(1, 1, rngs=rngs)
    ...     self.c = self.a  # shared Module
    ...
    >>> model = SharedModules(nnx.Rngs(0))
    >>> for duplicate_paths in nnx.find_duplicates(model):
    ...   print(duplicate_paths)
    [('a',), ('c',)]

  Args:
    node: A graph node object.
    only: A Filter to specify which nodes or leaves to consider for duplicates.
  Returns:
    A list of lists, where each inner list contains the different paths for a
    for a duplicate node or leaf.
  """
  node_paths: dict[int, list[PathParts]] = {}
  duplicate_candidate = filterlib.to_predicate(only)
  _node_paths(node, node_paths, (), duplicate_candidate)
  _duplicates = [paths for paths in node_paths.values() if len(paths) > 1]
  return _duplicates

