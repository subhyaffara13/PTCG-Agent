
def compact_name_scope(fun: _CallableT) -> _CallableT:
  """Creates compact submodules from a method.

  This is a decorator that allows you to define compact submodules from a
  method. It's intention is to make it easier to port code Haiku code to Flax
  by providing the same functionality.

  Example::

    >>> import flax.linen as nn
    >>> import jax
    >>> import jax.numpy as jnp
    >>> from flax.core import pretty_repr
    ...
    >>> class Foo(nn.Module):
    ...   @nn.compact_name_scope
    ...   def up(self, x):
    ...     return nn.Dense(3)(x)
    ...
    ...   @nn.compact_name_scope
    ...   def down(self, x):
    ...     return nn.Dense(3)(x)
    ...
    ...   def __call__(self, x):
    ...     return self.up(x) + self.down(x)
    ...
    >>> module = Foo()
    >>> variables = module.init(jax.random.PRNGKey(0), jnp.ones((1, 2)))
    >>> params = variables['params']
    >>> print(pretty_repr(jax.tree_util.tree_map(jnp.shape, params)))
    {
        down: {
            Dense_0: {
                bias: (3,),
                kernel: (2, 3),
            },
        },
        up: {
            Dense_0: {
                bias: (3,),
                kernel: (2, 3),
            },
        },
    }

  You can also use ``compact_name_scope`` inside ``@compact`` methods or even
  other
  ``compact_name_scope`` methods. Methods that are decorated with
  ``compact_name_scope``
  can also be called directly from ``init`` or ``apply`` via the ``method``
  argument::

    >>> y_down = module.apply({'params': params}, jnp.ones((1, 2)), method='down')
    >>> y_down.shape
    (1, 3)

  Args:
    fun: The Module method to mark as compact_name_scope.

  Returns:
    The given function ``fun`` marked as compact_name_scope.
  """

  @functools.wraps(fun)
  def compact_name_scope_wrapper(self: nn.Module, *args, **kwargs):
    name = fun.__name__
    if not hasattr(self, '_compact_name_scope_modules'):
      raise ValueError(
        f'Cannot call compact_name_scope method {name!r} on a Module that has not been '
        f'setup. This is likely because you are calling {name!r} '
        'from outside of init or apply.'
      )
    module = self._compact_name_scope_modules[name]
    return module(*args, **kwargs)

  compact_name_scope_wrapper.compact_name_scope = True  # type: ignore[attr-defined]
  compact_name_scope_wrapper.inner_fun = fun  # type: ignore[attr-defined]
  compact_name_scope_wrapper.nowrap = True  # type: ignore[attr-defined]
  return compact_name_scope_wrapper  # type: ignore[return-value]

