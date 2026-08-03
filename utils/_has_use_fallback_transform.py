import re
from typing import Dict

def _has_use_fallback_transform(
    input_key: TupleKey, flat_transforms: Dict[TupleKey, Transform]
) -> bool:
  result = False
  for transform_key, transform in flat_transforms.items():
    match = re.fullmatch(_keystr(transform_key), _keystr(input_key))
    if match and transform.use_fallback:
      result = True
  return result

