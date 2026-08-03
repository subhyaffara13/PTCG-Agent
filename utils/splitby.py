from typing import Callable

def splitby(
    iterable: Iterable[_T], predicate: Callable[[_T], bool]
) -> tuple[list[_T], list[_T]]:
  """Split the iterable into 2 lists (false, true), based on the predicate.

  Example:

  ```python
  small, big = epy.splitby([100, 4, 4, 1, 200], lambda x: x > 10)
  assert small == [4, 4, 1]
  assert big == [100, 200]
  ```

  Args:
    iterable: The iterable to split
    predicate: Function applied to split

  Returns:
    False list, True list
  """
  false_list = []
  true_list = []
  for v in iterable:
    if predicate(v):
      true_list.append(v)
    else:
      false_list.append(v)
  return false_list, true_list

