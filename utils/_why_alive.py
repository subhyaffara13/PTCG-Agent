from typing import Any

def _why_alive(ignore_ids: set[int], x: Any) -> str:
  parents = lambda x: [r for r in gc.get_referrers(x) if id(r) not in ignore_ids]
  child, lines, seen = x, [], set()
  while (id(child) not in seen and type(child) is not types.ModuleType
         and parents(child)):
    parent = parents(child)[0]  # just pick one parent

    # For namespaces (like modules and class instances) and closures, the
    # references may form a simple chain: e.g. instance refers to its own
    # __dict__ which refers to child, or function refers to its __closure__
    # which refers to cells which refer to child. In these cases, we can provide
    # a more intuitive description by collapsing the chain into a single
    # parent->child jump. We do that by setting `parent` here to be a
    # grandparent (or great-grandparent) of `child`, and then handling that case
    # in _why_alive_container_info. See example:
    #  https://github.com/jax-ml/jax/pull/13022#discussion_r1008456599
    # To prevent this collapsing behavior, just comment out this code block.
    if (isinstance(parent, dict) and
        getattr(parents(parent)[0], '__dict__', None) is parents(child)[0]):
      parent = parents(parent)[0]
    elif type(parent) is types.CellType:
      parent = parents(parents(parent)[0])[0]

    line = f'<{type(child).__name__} {id(child)}> is referred to by '
    lines.append(line + _why_alive_container_info(parent, id(child)))
    seen.add(id(child))
    child = parent
  return '\n' + '\n'.join(lines) if lines else ''

