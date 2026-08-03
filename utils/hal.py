import json

def hal(
    paths,
    exclude=_cfg.get_value('exclude', str, None),
    ignore=_cfg.get_value('ignore', str, None),
    json=False,
    functions=_cfg.get_value('functions', bool, False),
    output_file=_cfg.get_value('output_file', str, None),
    include_ipynb=_cfg.get_value('include_ipynb', bool, False),
    ipynb_cells=_cfg.get_value('ipynb_cells', bool, False),
):
    """
    Analyze the given Python modules and compute their Halstead metrics.

    The Halstead metrics are a series of measurements meant to quantitatively
    measure the complexity of code, including the difficulty a programmer would
    have in writing it.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -e, --exclude <str>: Exclude files only when their path matches one
        of these glob patterns. Usually needs quoting at the command line.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -j, --json: Format results in JSON.
    :param -f, --functions: Analyze files by top-level functions instead of as
        a whole.
    :param -O, --output-file <str>: The output file (default to stdout).
    :param --include-ipynb: Include IPython Notebook files
    :param --ipynb-cells: Include reports for individual IPYNB cells
    """
    config = Config(
        exclude=exclude,
        ignore=ignore,
        by_function=functions,
        include_ipynb=include_ipynb,
        ipynb_cells=ipynb_cells,
    )

    harvester = HCHarvester(paths, config)
    with outstream(output_file) as stream:
        log_result(harvester, json=json, xml=False, md=False, stream=stream)

