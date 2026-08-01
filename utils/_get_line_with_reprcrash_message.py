
def _get_line_with_reprcrash_message(
    config: Config, rep: BaseReport, tw: TerminalWriter, word_markup: dict[str, bool]
) -> str:
    """Get summary line for a report, trying to add reprcrash message."""
    verbose_word, verbose_markup = rep._get_verbose_word_with_markup(
        config, word_markup
    )
    word = tw.markup(verbose_word, **verbose_markup)
    node = _get_node_id_with_markup(tw, config, rep)

    line = f"{word} {node}"
    line_width = wcswidth(line)

    msg: str | None
    try:
        if isinstance(rep.longrepr, str):
            msg = rep.longrepr
        else:
            # Type ignored intentionally -- possible AttributeError expected.
            msg = rep.longrepr.reprcrash.message  # type: ignore[union-attr]
    except AttributeError:
        pass
    else:
        if (
            running_on_ci() or config.option.verbose >= 2
        ) and not config.option.force_short_summary:
            msg = f" - {msg}"
        else:
            available_width = tw.fullwidth - line_width
            msg = _format_trimmed(" - {}", msg, available_width)
        if msg is not None:
            line += msg

    return line

