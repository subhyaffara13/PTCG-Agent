
def report_messages_stats(
    sect: Section,
    stats: LinterStats,
    _: LinterStats | None,
) -> None:
    """Make messages type report."""
    by_msg_stats = stats.by_msg
    lines = ["message id", "occurrences"]
    for value, msg_id in sorted(
        (
            (value, msg_id)
            for msg_id, value in by_msg_stats.items()
            if not msg_id.startswith("I")
        ),
        reverse=True,
    ):
        lines += [msg_id, str(value)]
    sect.append(Table(children=lines, cols=2, rheaders=1))

