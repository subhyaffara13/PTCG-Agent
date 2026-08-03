from typing import Any

def _tree_trim(
    path: tuple[str | int, ...],
    template: PyTreeOf[Any],
    structure: PyTreeOf[T],
    trimmed_structure_callback: TrimmedStructureCallback[T] | None = None,
    strict: bool = True,
    allow_sequence_mapping_alignment: bool = False,
) -> PyTreeOf[T]:
  match template:
    # This wants to be `case abc.Mapping()` but http://b/283787842.
    case mapping if isinstance(mapping, abc.Mapping):
      is_list = isinstance(structure, list)
      is_standard_tuple = isinstance(
          structure, tuple
      ) and not utils.isinstance_of_namedtuple(structure)
      is_standard_sequence = is_list or is_standard_tuple

      if isinstance(structure, abc.Mapping):
        structure_dict = structure
      elif structure is None:
        structure_dict = {}
      elif utils.is_jax_internal_node(structure) and (
          allow_sequence_mapping_alignment or not is_standard_sequence
      ):
        flat_node = _jax_internal_node_to_dict(structure)
        structure_dict = flat_node.child_node_by_clean_key
        if trimmed_structure_callback:
          trimmed_structure_callback = _wrap_callback_for_conversion(
              trimmed_structure_callback,
              path,
              flat_node.original_key_by_clean_key,
          )
      else:
        raise TypeError(
            f'Type mismatch at key path {path}: template has type'
            f' {type(template)}, but structure has type {type(structure)}.'
        )

      keep_items = []
      drop_items = []
      placeholder_items = []

      if missing := [k for k in template if k not in structure_dict]:
        if strict:
          raise ValueError(
              f'Missing {len(missing)} keys in structure path {path}, '
              f'including: {missing[:10]}'
          )
        else:
          # Fill the result with placeholders
          placeholder_items.extend(
              (k, jax.tree.map(lambda x: ..., template[k])) for k in missing
          )

      for k, n in structure_dict.items():
        (keep_items if k in template else drop_items).append((k, n))

      if trimmed_structure_callback:
        for k, n in drop_items:
          trimmed_structure_callback((*path, k), n)

      keep_dict = {
          k: _tree_trim(
              (*path, k),
              template[k],
              v,
              trimmed_structure_callback,
              strict,
              allow_sequence_mapping_alignment,
          )
          for k, v in keep_items
      }
      return type(template)((*keep_dict.items(), *placeholder_items))  # pytype:disable=wrong-arg-count
    case named_tuple if utils.isinstance_of_namedtuple(named_tuple):
      if structure is None:
        structure = ()
      if isinstance(structure, abc.Mapping):
        children_dict = _tree_trim(
            path,
            named_tuple._asdict(),
            structure,
            trimmed_structure_callback,
            strict,
            allow_sequence_mapping_alignment,
        )
        return type(template)(**children_dict)
      elif isinstance(structure, abc.Sequence):
        children_sequence = _tree_trim(
            path,
            tuple(named_tuple),
            structure,
            trimmed_structure_callback,
            strict,
            allow_sequence_mapping_alignment,
        )
        return type(template)(*children_sequence)
      else:
        raise TypeError(
            f'Type mismatch at key path {path}: template has type'
            f' {type(template)}, but structure has type {type(structure)}.'
        )
    # This wants to be `case abc.Sequence()` but http://b/283787842.
    case sequence if isinstance(sequence, abc.Sequence) and not isinstance(
        sequence, str
    ):
      if structure is None:
        structure = ()
      elif not isinstance(structure, abc.Sequence):
        raise TypeError(
            f'Type mismatch at key path {path}: template has type'
            f' {type(template)}, but structure has type {type(structure)}'
        )
      if len(structure) != len(template):
        raise ValueError(
            f'Length mismatch at key path {path}: template has length'
            f' {len(template)}, but structure has length {len(structure)}'
        )
      elements = (
          _tree_trim(
              (*path, i),
              t,
              s,
              trimmed_structure_callback,
              strict,
              allow_sequence_mapping_alignment,
          )
          for i, (t, s) in enumerate(zip(template, structure))
      )
      return type(template)(elements)  # pytype:disable=wrong-arg-count
    case n if n is not None and utils.is_jax_internal_node(n):
      s_flat = _jax_internal_node_to_dict(structure)
      t_flat = _jax_internal_node_to_dict(template)

      if trimmed_structure_callback:
        wrapped_callback = _wrap_callback_for_conversion(
            trimmed_structure_callback, path, s_flat.original_key_by_clean_key
        )
      else:
        wrapped_callback = None

      # Note: unlike other cases, this does not treat the children
      # individually. Instead we have effectively cast the structure and
      # the template to mappings and will deal with them in their entirety
      # by reusing the mapping case.
      children_dict = _tree_trim(
          path,
          t_flat.child_node_by_clean_key,
          s_flat.child_node_by_clean_key,
          wrapped_callback,
          strict,
          allow_sequence_mapping_alignment,
      )
      # Now cast back to the result type.
      children = [
          children_dict[k] for k in t_flat.child_node_by_clean_key.keys()
      ]
      return jax.tree_util.tree_unflatten(t_flat.tree_def, children)
    case None:
      # None is special: it's the only type of template tree node that can
      # match both leaves and internal nodes of the structure to be trimmed.
      if utils.is_leaf_node(structure):
        if trimmed_structure_callback:
          trimmed_structure_callback(path, structure)
        return None
      else:
        _tree_trim(
            path,
            {},
            structure,
            trimmed_structure_callback,
            strict,
            allow_sequence_mapping_alignment,
        )
      return None
    case v if utils.is_leaf_node(v):
      if not utils.is_leaf_node_or_none(structure):
        raise TypeError(
            f'Type mismatch at key path {path}: template has type'
            f' {type(template)}, but structure has type {type(structure)}.'
        )
      return structure
    case _:
      raise TypeError(
          f'Unknown type at key path {path}: structure has type'
          f' {type(structure)}.'
      )

