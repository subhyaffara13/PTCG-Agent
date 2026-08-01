
def nowrap(fun: _CallableT) -> _CallableT:
  """Marks the given module method as a helper method that needn't be wrapped.

  Methods wrapped in ``@nowrap`` are private helper methods that needn't be wrapped
  with the state handler or a separate named_call transform.

  This is needed in several concrete instances:
   - if you're subclassing a method like Module.param and don't want this
     overridden core function decorated with the state management wrapper.
   - If you want a method to be callable from an unbound Module (e.g.: a
     function of construction of arguments that doesn't depend on params/RNGs).
     If you want to learn more about how Flax Modules manage their state read the
     [The Flax Module lifecycle](https://flax.readthedocs.io/en/latest/developer_notes/module_lifecycle.html)
     guide.

  For instance::

    >>> import flax.linen as nn
    >>> import jax, jax.numpy as jnp

    >>> class Foo(nn.Module):
    ...   num_features: int

    ...   @nn.nowrap
    ...   def _make_dense(self, num_features):
    ...     return nn.Dense(num_features)

    ...   @nn.compact
    ...   def __call__(self, x):
    ...     # now safe to use constructor helper even if using named_call
    ...     dense = self._make_dense(self.num_features)
    ...     return dense(x)

  Args:
    fun: The Module method to mark as nowrap.

  Returns:
    The given function ``fun`` marked as nowrap.
  """
  fun.nowrap = True  # type: ignore[attr-defined]
  return fun

