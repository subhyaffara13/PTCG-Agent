from typing import Any

def merge_nested_ts_specs(dict1: dict[Any, Any], dict2: dict[Any, Any] | None):
  """Merge two ts specs, dict2 takes precedence."""
  if dict2 is None:  # nothing to do
    return dict1
  # TODO(rdyro): this is an opinionated merge, we should get user feedback
  # merge kvstore explicitly
  kvstore = dict1.get("kvstore", {}) | dict2.get("kvstore", {})
  return dict1 | dict(dict2, kvstore=kvstore)  # merge with dict2 preferred

