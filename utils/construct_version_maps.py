from typing import Any

def construct_version_maps(
    upgrader_bytecode_function_to_index_map: dict[str, Any],
) -> str:
    version_map = torch._C._get_operator_version_map()
    sorted_version_map_ = sorted(version_map.items(), key=itemgetter(0))  # type: ignore[no-any-return]
    sorted_version_map = dict(sorted_version_map_)

    operator_list_in_version_map_part = []
    for op_name in sorted_version_map:
        upgraders_in_version_map_part = []
        # TODO: remove the skip after these two operators schemas are fixed
        if op_name in EXCLUDED_OP_SET:
            continue
        upgrader_ranges = torch._C._get_upgrader_ranges(op_name)
        upgrader_entries = sorted_version_map[op_name]
        if len(upgrader_ranges) != len(upgrader_entries):
            raise AssertionError(
                f"upgrader_ranges and upgrader_entries length mismatch for {op_name}: "
                f"{len(upgrader_ranges)} != {len(upgrader_entries)}"
            )
        for idx, upgrader_entry in enumerate(upgrader_entries):
            upgrader_name = upgrader_entry.upgrader_name
            bytecode_function_index = upgrader_bytecode_function_to_index_map[
                upgrader_name
            ]
            upgraders_in_version_map_part.append(
                ONE_UPGRADER_IN_VERSION_MAP.substitute(
                    upgrader_min_version=upgrader_ranges[idx].min_version,
                    upgrader_max_version=upgrader_ranges[idx].max_version,
                    upgrader_name=upgrader_name,
                    bytecode_func_index=bytecode_function_index,
                )
            )
        operator_list_in_version_map_part.append(
            ONE_OPERATOR_IN_VERSION_MAP.substitute(
                operator_name=op_name,
                upgrader_list_in_version_map="".join(upgraders_in_version_map_part),
            )
        )
    return OPERATOR_VERSION_MAP.substitute(
        operator_list_in_version_map="".join(operator_list_in_version_map_part).lstrip(
            "\n"
        )
    )

