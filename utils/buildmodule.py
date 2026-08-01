
def buildmodule(m, um):
    """
    Return
    """
    outmess(f"    Building module \"{m['name']}\"...\n")
    ret = {}
    mod_rules = defmod_rules[:]
    vrd = capi_maps.modsign2map(m)
    rd = dictappend({'f2py_version': f2py_version}, vrd)
    funcwrappers = []
    funcwrappers2 = []  # F90 codes
    for n in m['interfaced']:
        nb = None
        for bi in m['body']:
            if bi['block'] not in ['interface', 'abstract interface']:
                errmess('buildmodule: Expected interface block. Skipping.\n')
                continue
            for b in bi['body']:
                if b['name'] == n:
                    nb = b
                    break

        if not nb:
            print(
                f'buildmodule: Could not find the body of interfaced routine "{n}". Skipping.\n', file=sys.stderr)
            continue
        nb_list = [nb]
        if 'entry' in nb:
            for k, a in nb['entry'].items():
                nb1 = copy.deepcopy(nb)
                del nb1['entry']
                nb1['name'] = k
                nb1['args'] = a
                nb_list.append(nb1)
        for nb in nb_list:
            # requiresf90wrapper must be called before buildapi as it
            # rewrites assumed shape arrays as automatic arrays.
            isf90 = requiresf90wrapper(nb)
            # options is in scope here
            if options['emptygen']:
                b_path = options['buildpath']
                m_name = vrd['modulename']
                outmess('    Generating possibly empty wrappers"\n')
                Path(f"{b_path}/{vrd['coutput']}").touch()
                if isf90:
                    # f77 + f90 wrappers
                    outmess(f'    Maybe empty "{m_name}-f2pywrappers2.f90"\n')
                    Path(f'{b_path}/{m_name}-f2pywrappers2.f90').touch()
                    outmess(f'    Maybe empty "{m_name}-f2pywrappers.f"\n')
                    Path(f'{b_path}/{m_name}-f2pywrappers.f').touch()
                else:
                    # only f77 wrappers
                    outmess(f'    Maybe empty "{m_name}-f2pywrappers.f"\n')
                    Path(f'{b_path}/{m_name}-f2pywrappers.f').touch()
            api, wrap = buildapi(nb)
            if wrap:
                if isf90:
                    funcwrappers2.append(wrap)
                else:
                    funcwrappers.append(wrap)
            ar = applyrules(api, vrd)
            rd = dictappend(rd, ar)

    # Construct COMMON block support
    cr, wrap = common_rules.buildhooks(m)
    if wrap:
        funcwrappers.append(wrap)
    ar = applyrules(cr, vrd)
    rd = dictappend(rd, ar)

    # Construct F90 module support
    mr, wrap = f90mod_rules.buildhooks(m)
    if wrap:
        funcwrappers2.append(wrap)
    ar = applyrules(mr, vrd)
    rd = dictappend(rd, ar)

    for u in um:
        ar = use_rules.buildusevars(u, m['use'][u['name']])
        rd = dictappend(rd, ar)

    needs = cfuncs.get_needs()
    # Add mapped definitions
    needs['typedefs'] += [cvar for cvar in capi_maps.f2cmap_mapped  #
                          if cvar in typedef_need_dict.values()]
    code = {}
    for n in needs.keys():
        code[n] = []
        for k in needs[n]:
            c = ''
            if k in cfuncs.includes0:
                c = cfuncs.includes0[k]
            elif k in cfuncs.includes:
                c = cfuncs.includes[k]
            elif k in cfuncs.userincludes:
                c = cfuncs.userincludes[k]
            elif k in cfuncs.typedefs:
                c = cfuncs.typedefs[k]
            elif k in cfuncs.typedefs_generated:
                c = cfuncs.typedefs_generated[k]
            elif k in cfuncs.cppmacros:
                c = cfuncs.cppmacros[k]
            elif k in cfuncs.cfuncs:
                c = cfuncs.cfuncs[k]
            elif k in cfuncs.callbacks:
                c = cfuncs.callbacks[k]
            elif k in cfuncs.f90modhooks:
                c = cfuncs.f90modhooks[k]
            elif k in cfuncs.commonhooks:
                c = cfuncs.commonhooks[k]
            else:
                errmess(f'buildmodule: unknown need {repr(k)}.\n')
                continue
            code[n].append(c)
    mod_rules.append(code)
    for r in mod_rules:
        if ('_check' in r and r['_check'](m)) or ('_check' not in r):
            ar = applyrules(r, vrd, m)
            rd = dictappend(rd, ar)
    ar = applyrules(module_rules, rd)

    fn = os.path.join(options['buildpath'], vrd['coutput'])
    ret['csrc'] = fn
    with open(fn, 'w') as f:
        f.write(ar['modulebody'].replace('\t', 2 * ' '))
    outmess(f"    Wrote C/API module \"{m['name']}\" to file \"{fn}\"\n")

    if options['dorestdoc']:
        fn = os.path.join(
            options['buildpath'], vrd['modulename'] + 'module.rest')
        with open(fn, 'w') as f:
            f.write('.. -*- rest -*-\n')
            f.write('\n'.join(ar['restdoc']))
        outmess(f'    ReST Documentation is saved to file "{fn}"\n')
    if options['dolatexdoc']:
        fn = os.path.join(
            options['buildpath'], vrd['modulename'] + 'module.tex')
        ret['ltx'] = fn
        with open(fn, 'w') as f:
            f.write(
                f'% This file is auto-generated with f2py (version:{f2py_version})\n')
            if 'shortlatex' not in options:
                f.write(
                    '\\documentclass{article}\n\\usepackage{a4wide}\n\\begin{document}\n\\tableofcontents\n\n')
                f.write('\n'.join(ar['latexdoc']))
            if 'shortlatex' not in options:
                f.write('\\end{document}')
        outmess(f'    Documentation is saved to file "{fn}"\n')
    if funcwrappers:
        wn = os.path.join(options['buildpath'], vrd['f2py_wrapper_output'])
        ret['fsrc'] = wn
        with open(wn, 'w') as f:
            f.write('C     -*- fortran -*-\n')
            f.write(
                f'C     This file is autogenerated with f2py (version:{f2py_version})\n')
            f.write(
                'C     It contains Fortran 77 wrappers to fortran functions.\n')
            lines = []
            for l in ('\n\n'.join(funcwrappers) + '\n').split('\n'):
                if 0 <= l.find('!') < 66:
                    # don't split comment lines
                    lines.append(l + '\n')
                elif l and l[0] == ' ':
                    while len(l) >= 66:
                        lines.append(l[:66] + '\n     &')
                        l = l[66:]
                    lines.append(l + '\n')
                else:
                    lines.append(l + '\n')
            lines = ''.join(lines).replace('\n     &\n', '\n')
            f.write(lines)
        outmess(f'    Fortran 77 wrappers are saved to "{wn}\"\n')
    if funcwrappers2:
        wn = os.path.join(
            options['buildpath'], f"{vrd['modulename']}-f2pywrappers2.f90")
        ret['fsrc'] = wn
        with open(wn, 'w') as f:
            f.write('!     -*- f90 -*-\n')
            f.write(
                f'!     This file is autogenerated with f2py (version:{f2py_version})\n')
            f.write(
                '!     It contains Fortran 90 wrappers to fortran functions.\n')
            lines = []
            for l in ('\n\n'.join(funcwrappers2) + '\n').split('\n'):
                if 0 <= l.find('!') < 72:
                    # don't split comment lines
                    lines.append(l + '\n')
                elif len(l) > 72 and l[0] == ' ':
                    lines.append(l[:72] + '&\n     &')
                    l = l[72:]
                    while len(l) > 66:
                        lines.append(l[:66] + '&\n     &')
                        l = l[66:]
                    lines.append(l + '\n')
                else:
                    lines.append(l + '\n')
            lines = ''.join(lines).replace('\n     &\n', '\n')
            f.write(lines)
        outmess(f'    Fortran 90 wrappers are saved to "{wn}\"\n')
    return ret

