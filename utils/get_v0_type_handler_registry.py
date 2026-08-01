
def get_v0_type_handler_registry(
    leaf_handler_registry: types.LeafHandlerRegistry,
    context: context_lib.Context | None = None,
):
  """Returns a v0 type handler registry based on the `leaf_handler_registry`.

  Args:
    leaf_handler_registry: The LeafHandlerRegistry to be used to create a v0
      type handler registry.
    context: The Context to be used to default construct the LeafHandlers.
  """
  # register standardard v1 leaf handlers to the v0 type handler registry.
  handlers = []
  # We must reverse the order of the leaf handlers to ensure that the last
  # registered handler is the first one used as V1 registry is ordered by
  # priority of generic to specific, while V0 type handler registry is ordered
  # by the reverse.
  for leaf_type, _, leaf_handler_type in reversed(
      leaf_handler_registry.get_all()
  ):
    try:
      leaf_handler = leaf_handler_type(context=context)  # pytype: disable=wrong-keyword-args
    except TypeError as e:
      raise ValueError(
          f'Failed to default construct LeafHandler[{leaf_type}].  All'
          ' LeafHandler types must be able to be constructed with a context.'
      ) from e

    typestrs = leaf_handler_registry.get_secondary_typestrs(leaf_handler_type)
    typestr = typestrs[0] if typestrs else types.typestr(leaf_handler_type)
    handlers.append((
        leaf_type,
        CompatibleTypeHandler(
            leaf_handler,
            typestr=typestr,
        ),
    ))
  return type_handler_registry.create_type_handler_registry(*handlers)

