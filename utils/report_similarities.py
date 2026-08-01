
def report_similarities(
    sect: Section,
    stats: LinterStats,
    old_stats: LinterStats | None,
) -> None:
    """Make a layout with some stats about duplication."""
    lines = ["", "now", "previous", "difference"]
    lines += table_lines_from_stats(stats, old_stats, "duplicated_lines")
    sect.append(Table(children=lines, cols=4, rheaders=1, cheaders=1))

