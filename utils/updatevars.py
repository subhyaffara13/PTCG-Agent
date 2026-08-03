import copy
import re

def updatevars(typespec, selector, attrspec, entitydecl):
    """
    Returns last_name, the variable name without special chars, parenthesis
        or dimension specifiers.

    Alters groupcache to add the name, typespec, attrspec (and possibly value)
    of current variable.
    """
    global groupcache, groupcounter

    last_name = None
    kindselect, charselect, typename = cracktypespec(typespec, selector)
    # Clean up outer commas, whitespace and undesired chars from attrspec
    if attrspec:
        attrspec = [x.strip() for x in markoutercomma(attrspec).split('@,@')]
        l = []
        c = re.compile(r'(?P<start>[a-zA-Z]+)')
        for a in attrspec:
            if not a:
                continue
            m = c.match(a)
            if m:
                s = m.group('start').lower()
                a = s + a[len(s):]
            l.append(a)
        attrspec = l
    el = [x.strip() for x in markoutercomma(entitydecl).split('@,@')]
    el1 = []
    for e in el:
        for e1 in [x.strip() for x in markoutercomma(removespaces(markinnerspaces(e)), comma=' ').split('@ @')]:
            if e1:
                el1.append(e1.replace('@_@', ' '))
    for e in el1:
        m = namepattern.match(e)
        if not m:
            outmess(
                f'updatevars: no name pattern found for entity={repr(e)}. Skipping.\n')
            continue
        ename = rmbadname1(m.group('name'))
        edecl = {}
        if ename in groupcache[groupcounter]['vars']:
            edecl = groupcache[groupcounter]['vars'][ename].copy()
            not_has_typespec = 'typespec' not in edecl
            if not_has_typespec:
                edecl['typespec'] = typespec
            elif typespec and (not typespec == edecl['typespec']):
                current_typespec = edecl['typespec']
                outmess(f'updatevars: attempt to change the type of "{ename}" '
                        f'("{current_typespec}") to "{typespec}". Ignoring.\n')
            if 'kindselector' not in edecl:
                edecl['kindselector'] = copy.copy(kindselect)
            elif kindselect:
                for k in list(kindselect.keys()):
                    if k in edecl['kindselector'] and (not kindselect[k] == edecl['kindselector'][k]):
                        current_kind = edecl['kindselector'][k]
                        outmess('updatevars: attempt to change the kindselector '
                                f'"{k}" of "{ename}" ("{current_kind}") to '
                                f'"{kindselect[k]}". Ignoring.\n')
                    else:
                        edecl['kindselector'][k] = copy.copy(kindselect[k])
            if 'charselector' not in edecl and charselect:
                if not_has_typespec:
                    edecl['charselector'] = charselect
                else:
                    errmess(f'updatevars:{ename}: attempt to change empty charselector '
                            f'to {charselect!r}. Ignoring.\n')
            elif charselect:
                for k in list(charselect.keys()):
                    if k in edecl['charselector'] and (not charselect[k] == edecl['charselector'][k]):
                        outmess(f'updatevars: attempt to change the charselector "{k}" '
                                f'of "{ename}" ("{edecl["charselector"][k]}") to '
                                f'"{charselect[k]}". Ignoring.\n')
                    else:
                        edecl['charselector'][k] = copy.copy(charselect[k])
            if 'typename' not in edecl:
                edecl['typename'] = typename
            elif typename and (not edecl['typename'] == typename):
                outmess(f'updatevars: attempt to change the typename of "{ename}" '
                        f'("{edecl["typename"]}") to "{typename}". Ignoring.\n')
            if 'attrspec' not in edecl:
                edecl['attrspec'] = copy.copy(attrspec)
            elif attrspec:
                for a in attrspec:
                    if a not in edecl['attrspec']:
                        edecl['attrspec'].append(a)
        else:
            edecl['typespec'] = copy.copy(typespec)
            edecl['kindselector'] = copy.copy(kindselect)
            edecl['charselector'] = copy.copy(charselect)
            edecl['typename'] = typename
            edecl['attrspec'] = copy.copy(attrspec)
        if 'external' in (edecl.get('attrspec') or []) and e in groupcache[groupcounter]['args']:
            if 'externals' not in groupcache[groupcounter]:
                groupcache[groupcounter]['externals'] = []
            groupcache[groupcounter]['externals'].append(e)
        if m.group('after'):
            m1 = lenarraypattern.match(markouterparen(m.group('after')))
            if m1:
                d1 = m1.groupdict()
                for lk in ['len', 'array', 'init']:
                    if d1[lk + '2'] is not None:
                        d1[lk] = d1[lk + '2']
                        del d1[lk + '2']
                for k in list(d1.keys()):
                    if d1[k] is not None:
                        d1[k] = unmarkouterparen(d1[k])
                    else:
                        del d1[k]

                if 'len' in d1 and 'array' in d1:
                    if d1['len'] == '':
                        d1['len'] = d1['array']
                        del d1['array']
                    elif typespec == 'character':
                        if ('charselector' not in edecl) or (not edecl['charselector']):
                            edecl['charselector'] = {}
                        if 'len' in edecl['charselector']:
                            del edecl['charselector']['len']
                        edecl['charselector']['*'] = d1['len']
                        del d1['len']
                    else:
                        d1['array'] = d1['array'] + ',' + d1['len']
                        del d1['len']
                        array_spec = d1['array']
                        errmess(f'updatevars: "{typespec} {e}" is mapped to '
                                f'"{typespec} {ename}({array_spec})"\n')

                if 'len' in d1:
                    if typespec in ['complex', 'integer', 'logical', 'real']:
                        if ('kindselector' not in edecl) or (not edecl['kindselector']):
                            edecl['kindselector'] = {}
                        edecl['kindselector']['*'] = d1['len']
                        del d1['len']
                    elif typespec == 'character':
                        if ('charselector' not in edecl) or (not edecl['charselector']):
                            edecl['charselector'] = {}
                        if 'len' in edecl['charselector']:
                            del edecl['charselector']['len']
                        edecl['charselector']['*'] = d1['len']
                        del d1['len']

                if 'init' in d1:
                    if '=' in edecl and (not edecl['='] == d1['init']):
                        current_init = edecl['=']
                        new_init = d1['init']
                        outmess('updatevars: attempt to change the init expression of '
                                f'"{ename}" ("{current_init}") to "{new_init}". '
                                f'Ignoring.\n')
                    else:
                        edecl['='] = d1['init']

                if 'array' in d1:
                    dm = f"dimension({d1['array']})"
                    if 'attrspec' not in edecl or (not edecl['attrspec']):
                        edecl['attrspec'] = [dm]
                    else:
                        edecl['attrspec'].append(dm)
                        for dm1 in edecl['attrspec']:
                            if dm1[:9] == 'dimension' and dm1 != dm:
                                del edecl['attrspec'][-1]
                                errmess(f'updatevars:{ename}: attempt to change '
                                        f'{dm1!r} to {dm!r}. Ignoring.\n')
                                break

            else:
                outmess('updatevars: could not crack entity declaration "%s". Ignoring.\n' % (
                    ename + m.group('after')))
        for k in list(edecl.keys()):
            if not edecl[k]:
                del edecl[k]
        groupcache[groupcounter]['vars'][ename] = edecl
        if 'varnames' in groupcache[groupcounter]:
            groupcache[groupcounter]['varnames'].append(ename)
        last_name = ename
    return last_name

