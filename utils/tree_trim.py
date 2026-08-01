
def tree_trim(
    template: PyTreeOf[Any],
    structure: PyTreeOf[T],
    *,
    trimmed_structure_callback: TrimmedStructureCallback[T] | None = None,
    strict: Literal[False],
    allow_sequence_mapping_alignment: bool = False,
) -> parts_of.PartsOf[PyTreeOf[T]]:
  ...


def tree_trim(
    template: PyTreeOf[Any],
    structure: PyTreeOf[T],
    *,
    trimmed_structure_callback: TrimmedStructureCallback[T] | None = None,
    strict: Literal[True] = True,
    allow_sequence_mapping_alignment: bool = False,
) -> PyTreeOf[T]:
  ...


def tree_trim(
    template: PyTreeOf[Any],
    structure: PyTreeOf[T],
    *,
    trimmed_structure_callback: TrimmedStructureCallback[T] | None = None,
    strict: bool = True,
    allow_sequence_mapping_alignment: bool = False,
) -> PyTreeOf[T] | parts_of.PartsOf[PyTreeOf[T]]:
  """Removes nodes in `structure` so that its shape matches that of `template`.

  Only dictionary entries are trimmed; sequences are unchanged and the length
  of a sequence node in `structure` must match that of the corresponding node
  in `template`.

  If `not strict`, any subtree of a mapping or named tuple node of `template`
  that is missing from the corresponding node of `structure` will be replaced
  with an appropriately-shaped subtree full of `...` placeholders (Ellipsis)
  instead of causing an error. In this mode, the tree structure of the result
  is guaranteed to match the tree structure of `template`.

  Args:
    template: The tree whose shape is to be matched.
    structure: The tree to be trimmed.
    trimmed_structure_callback: If present, will be called with the path to, and
      value of, any node that is removed from `structure`.
    strict: Require every element of `template` to be matched by an element of
      `structure`.
    allow_sequence_mapping_alignment: If True, allows matching a Mapping
      template node with a Sequence structure node (converting the sequence to a
      dict first).

  Returns:
    A subset of `structure` that has the same shape as `template`.

  Raises:
    TypeError: If the type of a node in `structure` does not match the
      type of the corresponding node in `template`.
    ValueError: If keys in a dictionary node in `template` are not present
      in the corresponding node in `structure`, or if the length of a sequence
      node in `structure` does not match the length of the corresponding
      sequence node in `template`, or if an internal node that isn't a
      sequence or dictionary is encountered.
  """
  result = _tree_trim_impl(
      template,
      structure,
      trimmed_structure_callback=trimmed_structure_callback,
      strict=strict,
      allow_sequence_mapping_alignment=allow_sequence_mapping_alignment,
  )
  return result.full_structure if strict else result

