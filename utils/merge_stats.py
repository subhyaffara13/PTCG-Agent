
def merge_stats(stats: list[LinterStats]) -> LinterStats:
    """Used to merge multiple stats objects into a new one when pylint is run in
    parallel mode.
    """
    merged = LinterStats()
    for stat in stats:
        merged.bad_names["argument"] += stat.bad_names["argument"]
        merged.bad_names["attr"] += stat.bad_names["attr"]
        merged.bad_names["klass"] += stat.bad_names["klass"]
        merged.bad_names["class_attribute"] += stat.bad_names["class_attribute"]
        merged.bad_names["class_const"] += stat.bad_names["class_const"]
        merged.bad_names["const"] += stat.bad_names["const"]
        merged.bad_names["inlinevar"] += stat.bad_names["inlinevar"]
        merged.bad_names["function"] += stat.bad_names["function"]
        merged.bad_names["method"] += stat.bad_names["method"]
        merged.bad_names["module"] += stat.bad_names["module"]
        merged.bad_names["variable"] += stat.bad_names["variable"]
        merged.bad_names["typevar"] += stat.bad_names["typevar"]
        merged.bad_names["paramspec"] += stat.bad_names["paramspec"]
        merged.bad_names["typevartuple"] += stat.bad_names["typevartuple"]
        merged.bad_names["typealias"] += stat.bad_names["typealias"]

        for mod_key, mod_value in stat.by_module.items():
            merged.by_module[mod_key] = mod_value

        for msg_key, msg_value in stat.by_msg.items():
            try:
                merged.by_msg[msg_key] += msg_value
            except KeyError:
                merged.by_msg[msg_key] = msg_value

        merged.code_type_count["code"] += stat.code_type_count["code"]
        merged.code_type_count["comment"] += stat.code_type_count["comment"]
        merged.code_type_count["docstring"] += stat.code_type_count["docstring"]
        merged.code_type_count["empty"] += stat.code_type_count["empty"]
        merged.code_type_count["total"] += stat.code_type_count["total"]

        for dep_key, dep_value in stat.dependencies.items():
            try:
                merged.dependencies[dep_key].update(dep_value)
            except KeyError:
                merged.dependencies[dep_key] = dep_value

        merged.duplicated_lines["nb_duplicated_lines"] += stat.duplicated_lines[
            "nb_duplicated_lines"
        ]
        merged.duplicated_lines["percent_duplicated_lines"] += stat.duplicated_lines[
            "percent_duplicated_lines"
        ]

        merged.node_count["function"] += stat.node_count["function"]
        merged.node_count["klass"] += stat.node_count["klass"]
        merged.node_count["method"] += stat.node_count["method"]
        merged.node_count["module"] += stat.node_count["module"]

        merged.undocumented["function"] += stat.undocumented["function"]
        merged.undocumented["klass"] += stat.undocumented["klass"]
        merged.undocumented["method"] += stat.undocumented["method"]
        merged.undocumented["module"] += stat.undocumented["module"]

        merged.convention += stat.convention
        merged.error += stat.error
        merged.fatal += stat.fatal
        merged.info += stat.info
        merged.refactor += stat.refactor
        merged.statement += stat.statement
        merged.warning += stat.warning
        merged.skipped += stat.skipped

        merged.global_note += stat.global_note
    return merged

