
def cc(
    paths,
    min=_cfg.get_value('cc_min', str, 'A'),
    max=_cfg.get_value('cc_max', str, 'F'),
    show_complexity=_cfg.get_value('show_complexity', bool, False),
    average=_cfg.get_value('average', bool, False),
    exclude=_cfg.get_value('exclude', str, None),
    ignore=_cfg.get_value('ignore', str, None),
    order=_cfg.get_value('order', str, 'SCORE'),
    json=False,
    no_assert=_cfg.get_value('no_assert', bool, False),
    show_closures=_cfg.get_value('show_closures', bool, False),
    total_average=_cfg.get_value('total_average', bool, False),
    xml=False,
    md=False,
    codeclimate=False,
    output_file=_cfg.get_value('output_file', str, None),
    include_ipynb=_cfg.get_value('include_ipynb', bool, False),
    ipynb_cells=_cfg.get_value('ipynb_cells', bool, False),
):
    '''Analyze the given Python modules and compute Cyclomatic
    Complexity (CC).

    The output can be filtered using the *min* and *max* flags. In addition
    to that, by default complexity score is not displayed.

    :param paths: The paths where to find modules or packages to analyze. More
        than one path is allowed.
    :param -n, --min <str>: The minimum complexity to display (default to A).
    :param -x, --max <str>: The maximum complexity to display (default to F).
    :param -e, --exclude <str>: Exclude files only when their path matches one
        of these glob patterns. Usually needs quoting at the command line.
    :param -i, --ignore <str>: Ignore directories when their name matches one
        of these glob patterns: radon won't even descend into them. By default,
        hidden directories (starting with '.') are ignored.
    :param -s, --show-complexity: Whether or not to show the actual complexity
        score together with the A-F rank. Default to False.
    :param -a, --average: If True, at the end of the analysis display the
        average complexity. Default to False.
    :param --total-average: Like `-a, --average`, but it is not influenced by
        `min` and `max`. Every analyzed block is counted, no matter whether it
        is displayed or not.
    :param -o, --order <str>: The ordering function. Can be SCORE, LINES or
        ALPHA.
    :param -j, --json: Format results in JSON.
    :param --xml: Format results in XML (compatible with CCM).
    :param --md: Format results in Markdown.
    :param --codeclimate: Format results for Code Climate.
    :param --no-assert: Do not count `assert` statements when computing
        complexity.
    :param --show-closures: Add closures/inner classes to the output.
    :param -O, --output-file <str>: The output file (default to stdout).
    :param --include-ipynb: Include IPython Notebook files
    :param --ipynb-cells: Include reports for individual IPYNB cells
    '''
    config = Config(
        min=min.upper(),
        max=max.upper(),
        exclude=exclude,
        ignore=ignore,
        show_complexity=show_complexity,
        average=average,
        total_average=total_average,
        order=getattr(cc_mod, order.upper(), getattr(cc_mod, 'SCORE')),
        no_assert=no_assert,
        show_closures=show_closures,
        include_ipynb=include_ipynb,
        ipynb_cells=ipynb_cells,
    )
    harvester = CCHarvester(paths, config)
    with outstream(output_file) as stream:
        log_result(
            harvester,
            json=json,
            xml=xml,
            md=md,
            codeclimate=codeclimate,
            stream=stream,
        )

