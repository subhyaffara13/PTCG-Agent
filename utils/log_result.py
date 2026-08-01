
def log_result(harvester, **kwargs):
    '''Log the results of an :class:`~radon.cli.harvest.Harvester object.

    Keywords parameters determine how the results are formatted. If *json* is
    `True`, then `harvester.as_json()` is called. If *xml* is `True`, then
    `harvester.as_xml()` is called. If *codeclimate* is True, then
    `harvester.as_codeclimate_issues()` is called.
    Otherwise, `harvester.to_terminal()` is executed and `kwargs` is directly
    passed to the :func:`~radon.cli.log` function.
    '''
    if kwargs.get('json'):
        log(harvester.as_json(), noformat=True, **kwargs)
    elif kwargs.get('xml'):
        log(harvester.as_xml(), noformat=True, **kwargs)
    elif kwargs.get('codeclimate'):
        log_list(
            harvester.as_codeclimate_issues(),
            delimiter='\0',
            noformat=True,
            **kwargs
        )
    elif kwargs.get('md'):
        log(harvester.as_md(), noformat=True, **kwargs)
    else:
        for msg, h_args, h_kwargs in harvester.to_terminal():
            kw = kwargs.copy()
            kw.update(h_kwargs)
            if h_kwargs.get('error', False):
                log(msg, **kw)
                log_error(h_args[0], indent=1)
                continue
            msg = [msg] if not isinstance(msg, (list, tuple)) else msg
            log_list(msg, *h_args, **kw)

