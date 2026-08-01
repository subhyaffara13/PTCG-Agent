
def _get_node_id_with_markup(tw: TerminalWriter, config: Config, rep: BaseReport):
    nodeid = config.cwd_relative_nodeid(rep.nodeid)
    path, *parts = nodeid.split("::")
    if parts:
        parts_markup = tw.markup("::".join(parts), bold=True)
        return path + "::" + parts_markup
    else:
        return path

