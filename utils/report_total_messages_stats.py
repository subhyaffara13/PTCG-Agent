
def report_total_messages_stats(
    sect: Section,
    stats: LinterStats,
    previous_stats: LinterStats | None,
) -> None:
    """Make total errors / warnings report."""
    lines = ["type", "number", "previous", "difference"]
    lines += checkers.table_lines_from_stats(stats, previous_stats, "message_types")
    sect.append(Table(children=lines, cols=4, rheaders=1))

