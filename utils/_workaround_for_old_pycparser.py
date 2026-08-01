
def _workaround_for_old_pycparser(csource):
    # Workaround for a pycparser issue (fixed between pycparser 2.10 and
    # 2.14): "char*const***" gives us a wrong syntax tree, the same as
    # for "char***(*const)".  This means we can't tell the difference
    # afterwards.  But "char(*const(***))" gives us the right syntax
    # tree.  The issue only occurs if there are several stars in
    # sequence with no parenthesis in between, just possibly qualifiers.
    # Attempt to fix it by adding some parentheses in the source: each
    # time we see "* const" or "* const *", we add an opening
    # parenthesis before each star---the hard part is figuring out where
    # to close them.
    parts = []
    while True:
        match = _r_star_const_space.search(csource)
        if not match:
            break
        #print repr(''.join(parts)+csource), '=>',
        parts.append(csource[:match.start()])
        parts.append('('); closing = ')'
        parts.append(match.group())   # e.g. "* const "
        endpos = match.end()
        if csource.startswith('*', endpos):
            parts.append('('); closing += ')'
        level = 0
        i = endpos
        while i < len(csource):
            c = csource[i]
            if c == '(':
                level += 1
            elif c == ')':
                if level == 0:
                    break
                level -= 1
            elif c in ',;=':
                if level == 0:
                    break
            i += 1
        csource = csource[endpos:i] + closing + csource[i:]
        #print repr(''.join(parts)+csource)
    parts.append(csource)
    return ''.join(parts)

