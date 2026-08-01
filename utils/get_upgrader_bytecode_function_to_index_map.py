
def get_upgrader_bytecode_function_to_index_map(
    upgrader_dict: list[dict[str, Any]],
) -> dict[str, Any]:
    upgrader_bytecode_function_to_index_map = {}
    index = 0
    for upgrader_bytecode in upgrader_dict:
        for upgrader_name in upgrader_bytecode:
            if upgrader_name in EXCLUE_UPGRADER_SET:
                continue
            upgrader_bytecode_function_to_index_map[upgrader_name] = index
            index += 1
    return upgrader_bytecode_function_to_index_map

