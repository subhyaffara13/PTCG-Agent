
def find_param_docs(docstring):
    '''Find Sphinx's :param:, :type:, :returns:, and :rtype: lines and return
       a dictionary of the form:
       ``param: (opts, {metavar: meta, type: type, help: help})``.'''
    paramdocs = {}
    typedocs = {}
    for m in SPHINX_RE.finditer(docstring + '\n'):
        if m.group('field') in ['param',
                                'parameter',
                                'arg',
                                'argument',
                                'key',
                                'keyword']:
            # mando
            #     :param name: Help text.               name   None   None    0
            #     :param name <type>: Help text.        name   <type> None    1
            #     :param -n: Help text.                 -n     None   None    2
            #     :param -n <type>: Help text.          -n     <type> None    3
            #     :param --name: Help text.             --name None   None    4
            #     :param --name <type>: Help text.      --name <type> None    5
            #     :param -n, --name: Help text.         -n,    --name None    6
            #     :param -n, --name <type>: Help text.  -n,    --name <type>  7
            # sphinx
            #     :param name: Help text.               name   None   None    8
            #     :param type name: Help text.          type   name   None    9
            #     :type name: str

            # The following is ugly, but it allows for backward compatibility

            if m.group('var2') is None:  # 0, 2, 4, 8
                vname = m.group('var1')
                vtype = None
            # 1, 3, 5
            elif m.group('var2') is not None and '<' in m.group('var2'):
                vname = m.group('var1')
                vtype = m.group('var2')
            elif '-' in m.group('var1') and '-' in m.group('var2'):  # 6, 7
                vname = '{0} {1}'.format(m.group('var1'), m.group('var2'))
                vtype = m.group('var3')
            else:                        # 9
                vname = m.group('var2')
                vtype = m.group('var1')

            name, opts, meta = get_opts('{0} {1}'.format(vname.strip(),
                                                         vtype or ''))
            name = name.replace('-', '_')

            helpdoc = m.group('help').strip()
            helpdoc = helpdoc.splitlines(True)
            if len(helpdoc) > 1:
                helpdoc = helpdoc[0] + textwrap.dedent(''.join(helpdoc[1:]))
            else:
                helpdoc = helpdoc[0]
            paramdocs[name] = (opts, {
                'metavar': meta or None,
                'type': ARG_TYPE_MAP.get(meta.strip('<>')),
                'help': helpdoc,
            })
        elif m.group('field') == 'type':
            typedocs[m.group('var1').strip()] = m.group('help').strip()
    for key in typedocs:
        paramdocs[key][1]['type'] = ARG_TYPE_MAP.get(typedocs[key])
    return paramdocs

