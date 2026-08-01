
def getblocks(object, lstrip=False, enclosing=False, locate=False):
    """Return a list of source lines and starting line number for an object.
    Interactively-defined objects refer to lines in the interpreter's history.

    If enclosing=True, then also return any enclosing code.
    If lstrip=True, ensure there is no indentation in the first line of code.
    If locate=True, then also return the line number for the block of code.

    DEPRECATED: use 'getsourcelines' instead
    """
    lines, lnum = findsource(object)

    if ismodule(object):
        if lstrip: lines = _outdent(lines)
        return ([lines], [0]) if locate is True else [lines]

    #XXX: 'enclosing' means: closures only? or classes and files?
    indent = indentsize(lines[lnum])
    block = getblock(lines[lnum:]) #XXX: catch any TokenError here?

    if not enclosing or not indent:
        if lstrip: block = _outdent(block)
        return ([block], [lnum]) if locate is True else [block]

    pat1 = r'^(\s*def\s)|(.*(?<!\w)lambda(:|\s))'; pat1 = re.compile(pat1)
    pat2 = r'^(\s*@)'; pat2 = re.compile(pat2)
   #pat3 = r'^(\s*class\s)'; pat3 = re.compile(pat3) #XXX: enclosing class?
    #FIXME: bound methods need enclosing class (and then instantiation)
    #       *or* somehow apply a partial using the instance

    skip = 0
    line = 0
    blocks = []; _lnum = []
    target = ''.join(block)
    while line <= lnum: #XXX: repeat lnum? or until line < lnum?
        # see if starts with ('def','lambda') and contains our target block
        if pat1.match(lines[line]):
            if not skip:
                try: code = getblock(lines[line:])
                except TokenError: code = [lines[line]]
            if indentsize(lines[line]) > indent: #XXX: should be >= ?
                line += len(code) - skip
            elif target in ''.join(code):
                blocks.append(code) # save code block as the potential winner
                _lnum.append(line - skip) # save the line number for the match
                line += len(code) - skip
            else:
                line += 1
            skip = 0
        # find skip: the number of consecutive decorators
        elif pat2.match(lines[line]):
            try: code = getblock(lines[line:])
            except TokenError: code = [lines[line]]
            skip = 1
            for _line in code[1:]: # skip lines that are decorators
                if not pat2.match(_line): break
                skip += 1
            line += skip
        # no match: reset skip and go to the next line
        else:
            line +=1
            skip = 0

    if not blocks:
        blocks = [block]
        _lnum = [lnum]
    if lstrip: blocks = [_outdent(block) for block in blocks]
    # return last match
    return (blocks, _lnum) if locate is True else blocks

