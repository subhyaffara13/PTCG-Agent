from typing import Any, Callable

def dict_map(
    fn: Callable[[T], Any], dic: dict[Any, dict | list | tuple | T], leaf_type: type[T]
) -> dict[Any, dict | list | tuple | Any]:
    new_dict: dict[Any, dict | list | tuple | Any] = {}
    for k, v in dic.items():
        if isinstance(v, dict):
            new_dict[k] = dict_map(fn, v, leaf_type)
        else:
            new_dict[k] = tree_map(fn, v, leaf_type)

    return new_dict

