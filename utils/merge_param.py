
def merge_param(name: str, a: T | None, b: T | None) -> T:
  """Merges construction- and call-time argument.

  This is a utility for supporting a pattern where a Module hyperparameter
  can be passed either to ``__init__`` or ``__call__``, and the value that is
  not ``None`` will be used.

  Example::

    >>> import flax.linen as nn
    >>> from typing import Optional

    >>> class Foo(nn.Module):
    ...   train: Optional[bool] = None

    ...   def __call__(self, train: Optional[bool] = None):
    ...     train = nn.merge_param('train', self.train, train)

  An error is thrown when both arguments are ``None`` or both values are not
  ``None``.

  Args:
    name: the name of the parameter. Used for error messages.
    a: option a
    b: option b

  Returns:
    a or b whichever is not ``None``.
  """
  if a is None and b is None:
    raise ValueError(
      f'Parameter "{name}" must be passed to the constructor or at call time.'
    )
  if a is not None and b is not None:
    raise ValueError(
      f'Parameter "{name}" was passed to the constructor and at call time.'
      ' Should be passed just once.'
    )
  if a is None:
    assert b is not None
    return b
  return a

