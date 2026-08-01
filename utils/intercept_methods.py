
def intercept_methods(interceptor: Interceptor):
  # pylint: disable=g-doc-return-or-yield
  r"""Registers a new method interceptor.

  Method interceptors allow you to (at a distance) intercept method calls to
  modules. It works similarly to decorators. You could modify args/kwargs before
  calling the underlying method and/or modify the result returning from calling
  the underlying method. Or you could completely skip calling the underlying
  method and decide to do something differently.  For example::

    >>> import flax.linen as nn
    >>> import jax.numpy as jnp
    ...
    >>> class Foo(nn.Module):
    ...   def __call__(self, x):
    ...     return x
    ...
    >>> def my_interceptor1(next_fun, args, kwargs, context):
    ...   print('calling my_interceptor1')
    ...   return next_fun(*args, **kwargs)
    ...
    >>> foo = Foo()
    >>> with nn.intercept_methods(my_interceptor1):
    ...   _ = foo(jnp.ones([1]))
    calling my_interceptor1

  You could also register multiple interceptors on the same method. Interceptors
  will run in order. For example::

    >>> def my_interceptor2(next_fun, args, kwargs, context):
    ...   print('calling my_interceptor2')
    ...   return next_fun(*args, **kwargs)
    ...
    >>> with nn.intercept_methods(my_interceptor1), \
    ...      nn.intercept_methods(my_interceptor2):
    ...   _ = foo(jnp.ones([1]))
    calling my_interceptor1
    calling my_interceptor2

  You could skip other interceptors by directly calling the
  ``context.orig_method``. For example::

    >>> def my_interceptor3(next_fun, args, kwargs, context):
    ...   print('calling my_interceptor3')
    ...   return context.orig_method(*args, **kwargs)
    >>> with nn.intercept_methods(my_interceptor3), \
    ...      nn.intercept_methods(my_interceptor1), \
    ...      nn.intercept_methods(my_interceptor2):
    ...   _ = foo(jnp.ones([1]))
    calling my_interceptor3

  The following methods couldn't be intercepted:

  1. Methods decoratored with ``nn.nowrap``.
  2. Dunder methods including ``__eq__``, ``__repr__``, ``__init__``, ``__hash__``, and ``__post_init__``.
  3. Module dataclass fields.
  4. Module descriptors.

  Args:
    interceptor: A method interceptor.
  """
  _global_interceptor_stack.push(interceptor)
  try:
    yield
  finally:
    assert _global_interceptor_stack.pop() is interceptor

