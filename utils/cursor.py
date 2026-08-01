
def cursor(obj: A) -> Cursor[A]:
  """Wrap :class:`Cursor <flax.cursor.Cursor>` over ``obj`` and return it.
  Changes can then be applied to the Cursor object in the following ways:

  - single-line change via the ``.set`` method
  - multiple changes, and then calling the ``.build`` method
  - multiple changes conditioned on the pytree path and node value via the
    ``.apply_update`` method, and then calling the ``.build`` method

  ``.set`` example::

    >>> from flax.cursor import cursor

    >>> dict_obj = {'a': 1, 'b': (2, 3), 'c': [4, 5]}
    >>> modified_dict_obj = cursor(dict_obj)['b'][0].set(10)
    >>> assert modified_dict_obj == {'a': 1, 'b': (10, 3), 'c': [4, 5]}

  ``.build`` example::

    >>> from flax.cursor import cursor

    >>> dict_obj = {'a': 1, 'b': (2, 3), 'c': [4, 5]}
    >>> c = cursor(dict_obj)
    >>> c['b'][0] = 10
    >>> c['a'] = (100, 200)
    >>> modified_dict_obj = c.build()
    >>> assert modified_dict_obj == {'a': (100, 200), 'b': (10, 3), 'c': [4, 5]}

  ``.apply_update`` example::

    >>> from flax.cursor import cursor
    >>> from flax.training import train_state
    >>> import optax

    >>> def update_fn(path, value):
    ...   '''Replace params with empty dictionary.'''
    ...   if 'params' in path:
    ...     return {}
    ...   return value

    >>> state = train_state.TrainState.create(
    ...     apply_fn=lambda x: x,
    ...     params={'a': 1, 'b': 2},
    ...     tx=optax.adam(1e-3),
    ... )
    >>> c = cursor(state)
    >>> state2 = c.apply_update(update_fn).build()
    >>> assert state2.params == {}
    >>> assert state.params == {'a': 1, 'b': 2} # make sure original params are unchanged

  If the underlying ``obj`` is a ``list`` or ``tuple``, iterating over the Cursor object
  to get the child Cursors is also possible::

    >>> from flax.cursor import cursor

    >>> c = cursor(((1, 2), (3, 4)))
    >>> for child_c in c:
    ...   child_c[1] *= -1
    >>> assert c.build() == ((1, -2), (3, -4))

  View the docstrings for each method to see more examples of their usage.

  Args:
    obj: the object you want to wrap the Cursor in
  Returns:
    A Cursor object wrapped around obj.
  """
  return Cursor(obj, None)

