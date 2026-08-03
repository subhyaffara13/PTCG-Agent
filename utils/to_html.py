from typing import Any

def to_html(node: Any) -> str | None:
  """Extracts a rich HTML representation of node using _repr_html_."""
  repr_html_method = safely_get_real_method(node, '_repr_html_')
  if repr_html_method is None:
    return None
  html_for_node_and_maybe_metadata = repr_html_method()
  if isinstance(html_for_node_and_maybe_metadata, tuple):
    html_for_node, _ = html_for_node_and_maybe_metadata
  else:
    html_for_node = html_for_node_and_maybe_metadata
  return html_for_node


def to_html(nodes):
    listeners = []
    for i, n in enumerate(nodes):
        if n.context is None:
            continue
        s = _listener_template.format(id=str(i + 1), stack=escape(f'{n.label}:\n{n.context}'))
        listeners.append(s)
    dot = to_dot(nodes)
    return _template.replace('$DOT', repr(dot)).replace('$LISTENERS', '\n'.join(listeners))

