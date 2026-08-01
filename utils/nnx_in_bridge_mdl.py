
def nnx_in_bridge_mdl(factory: tp.Callable[[rnglib.Rngs], nnx_module.Module],
                      name: str | None = None) -> nnx_module.Module:
  """Make pure NNX modules a submodule of a bridge module.

  Create module at init time, or make abstract module and let parent bind
  it with its state.
  Use current bridge module scope for RNG generation.

  Args:
    factory: a function that takes an `nnx.Rngs` arg and returns an NNX module.
    name: the name of the module. Only used during `bridge.compact` functions;
      in setup() function the user will set it to an attribute explicitly.
  Returns:
    A submodule (`nnx.Module`) of the bridge module.
  """
  parent_ctx, parent = bdg_module.current_context(), bdg_module.current_module()
  assert parent_ctx is not None and parent is not None, 'nnx_in_bridge_mdl() only needed inside bridge Module'
  parent = parent_ctx.module
  assert parent.scope is not None

  if parent.is_initializing():
    module = factory(parent.scope.rngs)
  else:
    rngs = parent.scope.rngs if parent.scope.rngs else rnglib.Rngs(7)  # dummy
    module = nnx_eval_shape(factory, rngs, graph=True)

    @nnx_jit
    def rng_state(rngs):
      return graphlib.state(factory(rngs), rnglib.RngState, graph=True)

    # Make sure the internal rng state is not abstract - other vars shall be
    if parent.scope.rngs:
      graphlib.update(module, rng_state(parent.scope.rngs))

  # Automatically set the attribute if compact. If setup, user is responsible
  # for setting the attribute of the superlayer.
  if parent_ctx.in_compact:
    if name is None:
      name = bdg_module._auto_submodule_name(parent_ctx, type(module))
    setattr(parent, name, module)
  return module

