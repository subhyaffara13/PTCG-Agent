from typing import Any

def get_key_index(dct: dict[Any, Any], key: Any) -> int:
    # Ensure that we call dict.keys and not value.keys (which can call
    # overridden keys method). In the C++ guards, we relied on PyDict_Next
    # to traverse the dictionary, which uses the internal data structure and
    # does not call the overridden keys method.
    return list(builtin_dict_keys(dct)).index(key)

