from typing import List

def _int_list_flip_index_and_value(int_list: List[int]):
  """Reverses indices and values of a list of integers.

  Ex: [ 3, 4, 0, 1, 2 ] -> [ 2, 3, 4, 0, 1 ]
  Old index 0, value: 3 -> New index: 3, value: 0

  Args:
    int_list: List of integers.

  Returns:
    List of integers with reversed indices and values.
  """
  result = [None for _ in range(len(int_list))]
  for index, value in enumerate(int_list):
    result[value] = index
  assert None not in result
  return result

