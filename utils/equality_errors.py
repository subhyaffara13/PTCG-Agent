from typing import Any, Callable

def equality_errors(
    tree1: Any, tree2: Any, is_leaf: Callable[[Any], bool] | None = None,
) -> Iterable[tuple[KeyPath, str, str, str]]:
  """Helper to describe structural differences between two pytrees.

  Args:
    tree1, tree2: pytrees known to have different structure.

  Usage:

    raise Exception(
        "Value 1 and value 2 must have the same pytree structure, but they have "
        "the following structural differences:\n" +
        ("\n".join(
           f"   - {keystr(path)} is a {thing1} in value 1 and a {thing2} in "
           f" value 2, so {explanation}.\n"
           for path, thing1, thing2, explanation
           in equality_errors(val1, val2))))
  """
  yield from _equality_errors((), tree1, tree2, is_leaf)

