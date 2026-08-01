
def _get_priority(k: str, attr_priorities: dict[str, AttrPriority]) -> AttrPriority:
  return attr_priorities.get(k, AttrPriority.DEFAULT)

