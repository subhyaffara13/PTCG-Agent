
def _matchlambda(func, line):
    """check if lambda object 'func' matches raw line of code 'line'"""
    from .detect import code as getcode
    from .detect import freevars, globalvars, varnames
    dummy = lambda : '__this_is_a_big_dummy_function__'
    # process the line (removing leading whitespace, etc)
    lhs,rhs = line.split('lambda ',1)[-1].split(":", 1) #FIXME: if !1 inputs
    try: #FIXME: unsafe
        _ = eval("lambda %s : %s" % (lhs,rhs), globals(),locals())
    except Exception: _ = dummy
    # get code objects, for comparison
    _, code = getcode(_).co_code, getcode(func).co_code
    # check if func is in closure
    _f = [line.count(i) for i in freevars(func).keys()]
    if not _f: # not in closure
        # check if code matches
        if _ == code: return True
        return False
    # weak check on freevars
    if not all(_f): return False  #XXX: VERY WEAK
    # weak check on varnames and globalvars
    _f = varnames(func)
    _f = [line.count(i) for i in _f[0]+_f[1]]
    if _f and not all(_f): return False  #XXX: VERY WEAK
    _f = [line.count(i) for i in globalvars(func).keys()]
    if _f and not all(_f): return False  #XXX: VERY WEAK
    # check if func is a double lambda
    if (line.count('lambda ') > 1) and (lhs in freevars(func).keys()):
        _lhs,_rhs = rhs.split('lambda ',1)[-1].split(":",1) #FIXME: if !1 inputs
        try: #FIXME: unsafe
            _f = eval("lambda %s : %s" % (_lhs,_rhs), globals(),locals())
        except Exception: _f = dummy
        # get code objects, for comparison
        _, code = getcode(_f).co_code, getcode(func).co_code
        if len(_) != len(code): return False
        #NOTE: should be same code same order, but except for 't' and '\x88'
        _ = set((i,j) for (i,j) in zip(_,code) if i != j)
        if len(_) != 1: return False #('t','\x88')
        return True
    # check indentsize
    if not indentsize(line): return False #FIXME: is this a good check???
    # check if code 'pattern' matches
    #XXX: or pattern match against dis.dis(code)? (or use uncompyle2?)
    _ = _.split(_[0])  # 't' #XXX: remove matching values if starts the same?
    _f = code.split(code[0])  # '\x88'
    #NOTE: should be same code different order, with different first element
    _ = dict(re.match(r'([\W\D\S])(.*)', _[i]).groups() for i in range(1,len(_)))
    _f = dict(re.match(r'([\W\D\S])(.*)', _f[i]).groups() for i in range(1,len(_f)))
    if (_.keys() == _f.keys()) and (sorted(_.values()) == sorted(_f.values())):
        return True
    return False

