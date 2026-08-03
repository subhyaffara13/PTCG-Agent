from typing import Any

def add_to_call_tf_concrete_function_list(concrete_tf_fn: Any, call_tf_concrete_function_list: list[Any]) -> int:
  try:
    called_index = call_tf_concrete_function_list.index(concrete_tf_fn)
  except ValueError:
    called_index = len(call_tf_concrete_function_list)
    call_tf_concrete_function_list.append(concrete_tf_fn)
  return called_index

