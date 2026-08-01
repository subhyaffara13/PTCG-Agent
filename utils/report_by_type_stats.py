
def report_by_type_stats(
    sect: reporter_nodes.Section,
    stats: LinterStats,
    old_stats: LinterStats | None,
) -> None:
    """Make a report of.

    * percentage of different types documented
    * percentage of different types with a bad name
    """
    # percentage of different types documented and/or with a bad name
    nice_stats: dict[str, dict[str, str]] = {}
    for node_type in ("module", "class", "method", "function"):
        total = stats.get_node_count(node_type)
        nice_stats[node_type] = {}
        if total != 0:
            undocumented_node = stats.get_undocumented(node_type)
            documented = total - undocumented_node
            percent = (documented * 100.0) / total
            nice_stats[node_type]["percent_documented"] = f"{percent:.2f}"
            badname_node = stats.get_bad_names(node_type)
            percent = (badname_node * 100.0) / total
            nice_stats[node_type]["percent_badname"] = f"{percent:.2f}"
    lines = ["type", "number", "old number", "difference", "%documented", "%badname"]
    for node_type in ("module", "class", "method", "function"):
        node_type = cast(Literal["function", "class", "method", "module"], node_type)
        new = stats.get_node_count(node_type)
        old = old_stats.get_node_count(node_type) if old_stats else None
        diff_str = lint_utils.diff_string(old, new) if old else None
        lines += [
            node_type,
            str(new),
            str(old) if old else "NC",
            diff_str if diff_str else "NC",
            nice_stats[node_type].get("percent_documented", "0"),
            nice_stats[node_type].get("percent_badname", "0"),
        ]
    sect.append(reporter_nodes.Table(children=lines, cols=6, rheaders=1))

