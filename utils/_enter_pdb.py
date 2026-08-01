
def _enter_pdb(
    node: Node, excinfo: ExceptionInfo[BaseException], rep: BaseReport
) -> BaseReport:
    # XXX we reuse the TerminalReporter's terminalwriter
    # because this seems to avoid some encoding related troubles
    # for not completely clear reasons.
    tw = node.config.pluginmanager.getplugin("terminalreporter")._tw
    tw.line()

    showcapture = node.config.option.showcapture

    for sectionname, content in (
        ("stdout", rep.capstdout),
        ("stderr", rep.capstderr),
        ("log", rep.caplog),
    ):
        if showcapture in (sectionname, "all") and content:
            tw.sep(">", "captured " + sectionname)
            if content[-1:] == "\n":
                content = content[:-1]
            tw.line(content)

    tw.sep(">", "traceback")
    rep.toterminal(tw)
    tw.sep(">", "entering PDB")
    tb_or_exc = _postmortem_exc_or_tb(excinfo)
    rep._pdbshown = True  # type: ignore[attr-defined]
    post_mortem(tb_or_exc)
    return rep

