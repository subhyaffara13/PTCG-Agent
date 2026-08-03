from typing import Any

def construct_types(types_tr_list_from_yaml: list[Any]) -> str:
    types_tr_list_part = [
        ONE_TYPE.substitute(type_str=types_tr) for types_tr in types_tr_list_from_yaml
    ]
    if len(types_tr_list_part) == 0:
        return TYPE_LIST_EMPTY
    return TYPE_LIST.substitute(type_list="".join(types_tr_list_part).lstrip("\n"))

