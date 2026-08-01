
def linen_in_bridge_mdl(linen_module: nn_module.Module,
                        name: str | None = None) -> nnx_module.Module:
  """Make Linen modules a submodule of a bridge module using wrappers.ToNNX().

  Args:
    linen_module: the underlying Linen module instance.
    name: the name of the module. Only used during `bridge.compact` functions;
      in setup() function the user will set it to an attribute explicitly.
  Returns:
    A submodule (`nnx.Module`) of the bridge module.
  """
  parent_ctx, parent = bdg_module.current_context(), bdg_module.current_module()
  assert parent_ctx is not None and parent is not None, 'linen_in_bridge_mdl() only needed inside bridge Module'
  assert parent.scope is not None
  module = wrappers.ToNNX(linen_module, parent.scope.rngs)
  wrappers._set_initializing(module, parent.is_initializing())
  if parent_ctx.in_compact:
    if name is None:
      name = bdg_module._auto_submodule_name(parent_ctx, type(linen_module))
    setattr(parent, name, module)
  return module

