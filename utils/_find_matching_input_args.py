import re
from typing import Any, Dict, Optional

def _find_matching_input_args(
    input_key: TupleKey,
    flat_item: Dict[TupleKey, Any],
    flat_transforms: Dict[TupleKey, Transform],
    flat_restore_args: Dict[TupleKey, RestoreArgs],
) -> Optional[RestoreArgs]:
  """Given an input_key, tries to find matching RestoreArgs for the input.

  Args:
    input_key: A key in the input tree.
    flat_item: The flattened, user-provided item.
    flat_transforms: Flattened transformations dict.
    flat_restore_args: Flattened tree of RestoreArgs, relative to item.

  Returns:
    RestoreArgs that match the given input_key, according to the
    transformations, or None if no match is found.
  """
  for transform_key, transform in flat_transforms.items():
    if transform.multi_value_fn is not None:
      if not isinstance(transform, RestoreTransform):
        raise ValueError(
            'Must use RestoreTransform in order to use multi_value_fn'
            ' during restore.'
        )
      if transform.multi_value_fn_input_args is None:
        raise ValueError(
            '`multi_value_fn` was specified, but'
            ' `multi_value_fn_input_args` were not. The latter must be'
            ' specified to identify inputs for the function.'
        )
      for (
          input_key_regex,
          input_args,
      ) in transform.multi_value_fn_input_args.items():
        if re.fullmatch(input_key_regex, _keystr(input_key)):
          return input_args
    elif not transform.use_fallback:
      # The following is done to reverse-engineer the regex for the key in
      # the original tree.
      for output_key in flat_item:
        match = re.fullmatch(_keystr(transform_key), _keystr(output_key))
        if match:
          if transform.original_key is None:
            # If transform.original_key is not specified, this transform
            # does not rename the original key. We can reuse the key from
            # the item.
            input_key_pattern = _keystr(output_key)
          else:
            input_key_pattern = match.expand(transform.original_key)
          if input_key_pattern == _keystr(input_key):
            return flat_restore_args[output_key]
  return None

