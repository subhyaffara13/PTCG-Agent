
def crackline(line, reset=0):
    """
    reset=-1  --- initialize
    reset=0   --- crack the line
    reset=1   --- final check if mismatch of blocks occurred

    Cracked data is saved in grouplist[0].
    """
    global beginpattern, groupcounter, groupname, groupcache, grouplist
    global filepositiontext, currentfilename, neededmodule, expectbegin
    global skipblocksuntil, skipemptyends, previous_context, gotnextfile

    _, has_semicolon = split_by_unquoted(line, ";")
    if has_semicolon and not (f2pyenhancementspattern[0].match(line) or
                               multilinepattern[0].match(line)):
        # XXX: non-zero reset values need testing
        assert reset == 0, repr(reset)
        # split line on unquoted semicolons
        line, semicolon_line = split_by_unquoted(line, ";")
        while semicolon_line:
            crackline(line, reset)
            line, semicolon_line = split_by_unquoted(semicolon_line[1:], ";")
        crackline(line, reset)
        return
    if reset < 0:
        groupcounter = 0
        groupname = {groupcounter: ''}
        groupcache = {groupcounter: {}}
        grouplist = {groupcounter: []}
        groupcache[groupcounter]['body'] = []
        groupcache[groupcounter]['vars'] = {}
        groupcache[groupcounter]['block'] = ''
        groupcache[groupcounter]['name'] = ''
        neededmodule = -1
        skipblocksuntil = -1
        return
    if reset > 0:
        fl = 0
        if f77modulename and neededmodule == groupcounter:
            fl = 2
        while groupcounter > fl:
            outmess(f'crackline: groupcounter={groupcounter!r} groupname={groupname!r}\n')
            outmess(
                'crackline: Mismatch of blocks encountered. Trying to fix it by assuming "end" statement.\n')
            grouplist[groupcounter - 1].append(groupcache[groupcounter])
            grouplist[groupcounter - 1][-1]['body'] = grouplist[groupcounter]
            del grouplist[groupcounter]
            groupcounter = groupcounter - 1
        if f77modulename and neededmodule == groupcounter:
            grouplist[groupcounter - 1].append(groupcache[groupcounter])
            grouplist[groupcounter - 1][-1]['body'] = grouplist[groupcounter]
            del grouplist[groupcounter]
            groupcounter = groupcounter - 1  # end interface
            grouplist[groupcounter - 1].append(groupcache[groupcounter])
            grouplist[groupcounter - 1][-1]['body'] = grouplist[groupcounter]
            del grouplist[groupcounter]
            groupcounter = groupcounter - 1  # end module
            neededmodule = -1
        return
    if line == '':
        return
    flag = 0
    for pat in [dimensionpattern, externalpattern, intentpattern, optionalpattern,
                requiredpattern,
                parameterpattern, datapattern, publicpattern, privatepattern,
                intrinsicpattern,
                endifpattern, endpattern,
                formatpattern,
                beginpattern, functionpattern, subroutinepattern,
                implicitpattern, typespattern, commonpattern,
                callpattern, usepattern, containspattern,
                entrypattern,
                f2pyenhancementspattern,
                multilinepattern,
                moduleprocedurepattern
                ]:
        m = pat[0].match(line)
        if m:
            break
        flag = flag + 1
    if not m:
        re_1 = crackline_re_1
        if 0 <= skipblocksuntil <= groupcounter:
            return
        if 'externals' in groupcache[groupcounter]:
            for name in groupcache[groupcounter]['externals']:
                if name in invbadnames:
                    name = invbadnames[name]
                if 'interfaced' in groupcache[groupcounter] and name in groupcache[groupcounter]['interfaced']:
                    continue
                m1 = re.match(
                    rf'(?P<before>[^"]*)\b{name}\b\s*@\(@(?P<args>[^@]*)@\)@.*\Z',
                    markouterparen(line), re.I)
                if m1:
                    m2 = re_1.match(m1.group('before'))
                    a = _simplifyargs(m1.group('args'))
                    if m2:
                        line = f"callfun {name}({a}) result ({m2.group('result')})"
                    else:
                        line = f'callfun {name}({a})'
                    m = callfunpattern[0].match(line)
                    if not m:
                        outmess(
                            f'crackline: could not resolve function call for line={repr(line)}.\n')
                        return
                    analyzeline(m, 'callfun', line)
                    return
        if verbose > 1 or (verbose == 1 and currentfilename.lower().endswith('.pyf')):
            previous_context = None
            outmess(f'crackline:{groupcounter}: No pattern for line\n')
        return
    elif pat[1] == 'end':
        if 0 <= skipblocksuntil < groupcounter:
            groupcounter = groupcounter - 1
            if skipblocksuntil <= groupcounter:
                return
        if groupcounter <= 0:
            raise Exception(f'crackline: groupcounter(={groupcounter}) is nonpositive. '
                            'Check the blocks.')
        m1 = beginpattern[0].match(line)
        if (m1) and (not m1.group('this') == groupname[groupcounter]):
            raise Exception(f'crackline: End group {m1.group("this")!r} '
                            'does not match with previous Begin group '
                            f'{groupname[groupcounter]!r}\n\t{filepositiontext}')
        if skipblocksuntil == groupcounter:
            skipblocksuntil = -1
        grouplist[groupcounter - 1].append(groupcache[groupcounter])
        grouplist[groupcounter - 1][-1]['body'] = grouplist[groupcounter]
        del grouplist[groupcounter]
        groupcounter = groupcounter - 1
        if not skipemptyends:
            expectbegin = 1
    elif pat[1] == 'begin':
        if 0 <= skipblocksuntil <= groupcounter:
            groupcounter = groupcounter + 1
            return
        gotnextfile = 0
        analyzeline(m, pat[1], line)
        expectbegin = 0
    elif pat[1] == 'endif':
        pass
    elif pat[1] == 'moduleprocedure':
        analyzeline(m, pat[1], line)
    elif pat[1] == 'contains':
        if ignorecontains:
            return
        if 0 <= skipblocksuntil <= groupcounter:
            return
        skipblocksuntil = groupcounter
    else:
        if 0 <= skipblocksuntil <= groupcounter:
            return
        analyzeline(m, pat[1], line)

