
def _list_state_dict(xs: list[Any]) -> dict[str, Any]:
  return {str(i): to_state_dict(x) for i, x in enumerate(xs)}

