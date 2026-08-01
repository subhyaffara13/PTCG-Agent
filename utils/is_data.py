
def is_data(value: tp.Any, /) -> bool:
  """Checks if a value is a registered data type.

  This function checks a the value is registered data type, which means it is
  automatically recognized as data when assigned a :class:`flax.nnx.Pytree` attribute.

  Data types are:

  - ``jax.Array``
  - ``np.ndarray``
  - ``ArrayRef``
  - Variables (:class:`flax.nnx.Param`, :class:`flax.nnx.BatchStat`, `nnx.RngState`, etc.)
  - All graph nodes (:class:`flax.nnx.Object`, :class:`flax.nnx.Module`, :class:`flax.nnx.Rngs`, etc.)
  - Any type registered with :func:`flax.nnx.register_data_type`
  - Any pytree that contains at least one node or leaf element of the above


  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ... # ------ DATA ------------
    >>> assert nnx.is_data( jnp.array(0) )                      # Arrays
    >>> assert nnx.is_data( nnx.Param(1) )                      # Variables
    >>> assert nnx.is_data( nnx.Rngs(2) )                       # nnx.Pytrees
    >>> assert nnx.is_data( nnx.Linear(1, 1,rngs=nnx.Rngs(0)) ) # Modules
    ... # ------ STATIC ------------
    >>> assert not nnx.is_data( 'hello' )                       # strings, arbitrary objects
    >>> assert not nnx.is_data( 42 )                            # int, float, bool, complex, etc.
    >>> assert not nnx.is_data( [1, 2.0, 3j, jnp.array(1)] )    # list, dict, tuple, pytrees


  Args:
    value: The value to check.

  Returns:
    A string representing the attribute status.
  """
  return (
    graphlib.is_node_leaf(value)
    or graphlib.is_graph_node(value)
    or type(value) in DATA_REGISTRY
  )

