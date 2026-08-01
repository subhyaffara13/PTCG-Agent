
def update_context(tag: tp.Hashable):
  """Creates an :class:`UpdateContext` context manager which can be used to handle
  more complex state updates beyond what ``nnx.update`` can handle, including
  updates to static properties and graph structure.

  UpdateContext exposes a ``split`` and ``merge`` API with the same
  signature as ``nnx.split`` / ``nnx.merge`` but performs some bookkeeping
  to have the necessary information in order to perfectly update the input
  objects based on the changes made inside the transform. The UpdateContext
  must call split and merge a total of 4 times, the first
  and last calls happen outside the transform and the second and third calls
  happen inside the transform as shown in the diagram below::


                          idxmap
    (2) merge ─────────────────────────────► split (3)
          ▲                                    │
          │               inside               │
          │. . . . . . . . . . . . . . . . . . │ index_mapping
          │               outside              │
          │                                    ▼
    (1) split──────────────────────────────► merge (4)
                          refmap


  The first call to split ``(1)`` creates a ``refmap`` which keeps track of the
  outer references, and the first call to merge ``(2)`` creates an ``idxmap`` which
  keeps track of the inner references. The second call to split ``(3)`` combines
  the refmap and idxmap to produce the ``index_mapping`` which indicates
  how the outer references map to the inner references. Finally, the last call to
  merge ``(4)`` uses the index_mapping and the refmap to reconstruct the
  output of the transform while reusing/updating the inner references. To avoid
  memory leaks, the idxmap is cleared after ``(3)`` and the refmap is
  cleared after ``(4)``, and both are cleared after the context manager exits.

  Here is a simple example showing the use of ``update_context``::

    >>> from flax import nnx
    ...
    >>> class Foo(nnx.Module): pass
    ...
    >>> m1 = Foo()
    >>> with nnx.update_context('example'):
    ...   with nnx.split_context('example') as ctx:
    ...     graphdef, state = ctx.split(m1)
    ...   @jax.jit
    ...   def f(graphdef, state):
    ...     with nnx.merge_context('example', inner=True) as ctx:
    ...       m2 = ctx.merge(graphdef, state)
    ...     m2.a = 1
    ...     m2.ref = m2  # create a reference cycle
    ...     with nnx.split_context('example') as ctx:
    ...       return ctx.split(m2)
    ...   graphdef_out, state_out = f(graphdef, state)
    ...   with nnx.merge_context('example', inner=False) as ctx:
    ...     m3 = ctx.merge(graphdef_out, state_out)
    ...
    >>> assert m1 is m3
    >>> assert m1.a == 1
    >>> assert m1.ref is m1

  Note that ``update_context`` takes in a ``tag`` argument which is used
  primarily as a safety mechanism reduce the risk of accidentally using the
  wrong UpdateContext when using :func:`current_update_context` to access the
  current active context. ``update_context`` can also be used as a
  decorator that creates/activates an UpdateContext context for the
  duration of the function::

    >>> from flax import nnx
    ...
    >>> class Foo(nnx.Module): pass
    ...
    >>> m1 = Foo()
    >>> @jax.jit
    ... def f(graphdef, state):
    ...   with nnx.merge_context('example', inner=True) as ctx:
    ...     m2 = ctx.merge(graphdef, state)
    ...   m2.a = 1     # insert static attribute
    ...   m2.ref = m2  # create a reference cycle
    ...   with nnx.split_context('example') as ctx:
    ...     return ctx.split(m2)
    ...
    >>> @nnx.update_context('example')
    ... def g(m1):
    ...   with nnx.split_context('example') as ctx:
    ...     graphdef, state = ctx.split(m1)
    ...   graphdef_out, state_out = f(graphdef, state)
    ...   with nnx.merge_context('example', inner=False) as ctx:
    ...     return ctx.merge(graphdef_out, state_out)
    ...
    >>> m3 = g(m1)
    >>> assert m1 is m3
    >>> assert m1.a == 1
    >>> assert m1.ref is m1

  The context can be accessed using :func:`current_update_context`.

  Args:
    tag: A string tag to identify the context.
  """
  return UpdateContextManager(tag=tag)

