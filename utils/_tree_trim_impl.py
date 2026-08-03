import functools
from typing import Any

def _tree_trim_impl(
    template: PyTreeOf[Any],
    structure: PyTreeOf[T],
    *,
    trimmed_structure_callback: TrimmedStructureCallback[T] | None = None,
    strict: bool = True,
    allow_sequence_mapping_alignment: bool = False,
) -> parts_of.PartsOf[PyTreeOf[T]]:
  """Implementation of `tree_trim()` that always returns a `PartsOf`."""
  # To avoid a self-referential recursion, we create a partial that captures
  # the `trimmed_structure_callback` and `strict` arguments instead of doing an
  # implicit closure.
  tree_trim_fn = functools.partial(
      _tree_trim,
      trimmed_structure_callback=trimmed_structure_callback,
      strict=strict,
      allow_sequence_mapping_alignment=allow_sequence_mapping_alignment,
  )
  return parts_of.PartsOf(template, tree_trim_fn((), template, structure))

