
def share_scope(module: Module, other: Module, /):
  """Modifies one of the Modules such that they share the same scope. This is useful
  when you want to wrap a Module and extend its functionality without changing the
  parameter structure.

  ``share_scope`` takes two Modules, ``module`` and ``other``. ``module`` will use
  ``other``'s scope if ``other`` has a scope and its not a descendant of``module``'s
  scope::

    >>> import flax.linen as nn
    >>> import jax
    >>> from jax import numpy as jnp, random
    ...
    >>> class DenseLoRA(nn.Module):
    ...   base: nn.Dense
    ...   rank: int
    ...
    ...   def setup(self):
    ...     nn.share_scope(self, self.base)
    ...
    ...   @nn.compact
    ...   def __call__(self, x: jax.Array):
    ...     din, dout = x.shape[-1], self.base.features
    ...     A = self.param('A', nn.zeros_init(), (din, self.rank))
    ...     B = self.param('B', nn.zeros_init(), (self.rank, dout))
    ...     return self.base(x) + x @ A @ B
    ...
    >>> class Model(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x: jax.Array):
    ...     dense = nn.Dense(10) # base scope
    ...     return DenseLoRA(dense, rank=2)(x) # reuse the base scope
    ...
    >>> model = Model()
    ...
    >>> params = model.init(random.key(0), jnp.ones((1, 5)))['params']
    >>> list(params['Dense_0'].keys())
    ['A', 'B', 'kernel', 'bias']

  When ``other``'s scope is a descendant of ``module``'s scope then ``other``
  will use ``module``'s scope instead::

    >>> class DenseLoRA(nn.Module):
    ...   features: int
    ...   rank: int
    ...
    ...   def setup(self):
    ...     self.child = nn.Dense(self.features)
    ...     nn.share_scope(self, self.child)
    ...
    ...   @nn.compact
    ...   def __call__(self, x: jax.Array):
    ...     din, dout = x.shape[-1], self.features
    ...     A = self.param('A', nn.zeros_init(), (din, self.rank))
    ...     B = self.param('B', nn.zeros_init(), (self.rank, dout))
    ...     return self.child(x) + x @ A @ B
    ...
    >>> class Model(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x: jax.Array):
    ...     return DenseLoRA(10, rank=2)(x)
    ...
    >>> model = Model()
    ...
    >>> params = model.init(random.key(0), jnp.ones((1, 5)))['params']
    >>> list(params['DenseLoRA_0'].keys())
    ['A', 'B', 'kernel', 'bias']
  """
  if module.scope is None or other.scope is None:
    raise errors.CallShareScopeOnUnboundModuleError()

  def _is_child_scope(scope: Scope, other: Scope) -> bool:
    target: Scope | None = other

    while target is not None:
      if target is scope:
        return True
      target = target.parent
    return False

  if _is_child_scope(module.scope, other.scope):
    # Child is a true child, overwrite its scope
    module_to_update = other
    new_scope = module.scope
  else:
    # Child has its own independent scope, overwrite
    # parent scope, so that we preserve the sharing
    module_to_update = module
    new_scope = other.scope

  old_scope = module_to_update.scope
  object.__setattr__(module_to_update, 'scope', new_scope)

  # Reattach all the children to the new scope as well.
  for m in module_to_update._state.children.values():
    if not isinstance(m, Module):
      continue
    # Should we go recursively to check if any of the ancestors point to the old
    # scope?
    if m.scope and m.scope.parent == old_scope:
      # Reserve the scope, so that if there is a conflict we can raise an error.
      if isinstance(m.scope.name, str):
        new_scope.reserve(m.scope.name)
      m.scope.parent = new_scope

