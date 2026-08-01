
def raw(rawmode: str, data: Sequence[int] | bytes | bytearray) -> ImagePalette:
    palette = ImagePalette()
    palette.rawmode = rawmode
    palette.palette = data
    palette.dirty = 1
    return palette


def raw(
    paths,
    exclude=_cfg.get_value('exclude', str, None),
    ignore=_cfg.get_value('ignore', str, None),
    summary=False,
    json=False,
    output_file=_cfg.get_value('output_file', str, None),
    include_ipynb=_cfg.get_value('include_ipynb', bool, False),
    ipynb_cells=_cfg.get_value('ipynb_cells', bool, False),
):
    '''Analyze the given Python modules and compute raw metrics.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -e, --exclude <str>: Exclude files only when their path matches one
        of these glob patterns. Usually needs quoting at the command line.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -s, --summary:  If given, at the end of the analysis display the
        summary of the gathered metrics. Default to False.
    :param -j, --json: Format results in JSON. Note that the JSON export does
        not include the summary (enabled with `-s, --summary`).
    :param -O, --output-file <str>: The output file (default to stdout).
    :param --include-ipynb: Include IPython Notebook files
    :param --ipynb-cells: Include reports for individual IPYNB cells
    '''
    config = Config(
        exclude=exclude,
        ignore=ignore,
        summary=summary,
        include_ipynb=include_ipynb,
        ipynb_cells=ipynb_cells,
    )
    harvester = RawHarvester(paths, config)
    with outstream(output_file) as stream:
        log_result(harvester, json=json, stream=stream)


def raw(request):
    """raw keyword argument for rolling.apply"""
    return request.param

