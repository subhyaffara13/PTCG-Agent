
def _restore_type_by_abstract_type(
    abstract_checkpointable: Any,
) -> Any:
  """Allows users to override the restored type.

  When users pass the `value` in the `DeserializationParam`, the `PyTreeHandler`
  will try to restore to the specified type `T`. This only supports the standard
  types supported by Orbax.
  For example:
    - `jax.ShapeDtype` -> `jax.Array`
    - `NumpyAbstractType` -> `jax.Array`
    - `int` | `float` | `Type[int]` | `Type[float]` -> `int` | `float` | `int` |
    `float`

  Args:
    abstract_checkpointable: The abstract checkpointable passed in by the user.

  Returns:
    Returns the `restore_type` parameter for `V0RestoreArgs`. This is needed to
    determine which `LeafHandler` will eventually handle this
    `abstract_checkpointable`.
  """

  if abstract_checkpointable is None:
    ret = None
  elif serialization_types.is_placeholder(abstract_checkpointable):
    ret = serialization_types.PLACEHOLDER
  else:
    if isinstance(abstract_checkpointable, type):
      abstract_type = abstract_checkpointable
    else:
      abstract_type = type(abstract_checkpointable)

    # Make sure test with AbstractShardedArray before AbstractArray otherwise
    # Numpy will be matched first.
    if protocol_utils.is_subclass_protocol(
        abstract_type, serialization_types.AbstractShardedArray
    ):
      ret = jax.Array
    elif protocol_utils.is_subclass_protocol(
        abstract_type, serialization_types.AbstractArray
    ):
      ret = np.ndarray
    elif issubclass(abstract_type, get_args(scalar_leaf_handler.Scalar)):
      ret = abstract_type
    else:
      # this will use registered handler derived from metadata
      ret = None

  logging.vlog(
      1,
      'abstract_checkpointable: %s, restore_type: %s',
      abstract_checkpointable,
      ret,
  )
  return ret

