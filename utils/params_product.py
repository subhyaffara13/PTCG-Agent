import itertools
from typing import Any

def params_product(*params_lists: Sequence[Sequence[Any]],
                   named: bool = False) -> Sequence[Sequence[Any]]:
  """Generates a cartesian product of `params_lists`.

  See tests from ``variants_test.py`` for examples of usage.

  Args:
    *params_lists: A list of params combinations.
    named: Whether to generate test names (for
      `absl.parameterized.named_parameters(...)`).

  Returns:
    A cartesian product of `params_lists` combinations.
  """

  def generate():
    for combination in itertools.product(*params_lists):
      if named:
        name = "_".join(t[0] for t in combination)
        args_tuples = (t[1:] for t in combination)
        args = sum(args_tuples, ())
        yield (name, *args)
      else:
        yield sum(combination, ())

  return list(generate())

