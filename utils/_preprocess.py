
def _preprocess(csource):
    # First, remove the lines of the form '#line N "filename"' because
    # the "filename" part could confuse the rest
    csource, line_directives = _remove_line_directives(csource)
    # Remove comments.  NOTE: this only work because the cdef() section
    # should not contain any string literals (except in line directives)!
    def replace_keeping_newlines(m):
        return ' ' + m.group().count('\n') * '\n'
    csource = _r_comment.sub(replace_keeping_newlines, csource)
    # Remove the "#define FOO x" lines
    macros = {}
    for match in _r_define.finditer(csource):
        macroname, macrovalue = match.groups()
        macrovalue = macrovalue.replace('\\\n', '').strip()
        macros[macroname] = macrovalue
    csource = _r_define.sub('', csource)
    #
    if pycparser.__version__ < '2.14':
        csource = _workaround_for_old_pycparser(csource)
    #
    # BIG HACK: replace WINAPI or __stdcall with "volatile const".
    # It doesn't make sense for the return type of a function to be
    # "volatile volatile const", so we abuse it to detect __stdcall...
    # Hack number 2 is that "int(volatile *fptr)();" is not valid C
    # syntax, so we place the "volatile" before the opening parenthesis.
    csource = _r_stdcall2.sub(' volatile volatile const(', csource)
    csource = _r_stdcall1.sub(' volatile volatile const ', csource)
    csource = _r_cdecl.sub(' ', csource)
    #
    # Replace `extern "Python"` with start/end markers
    csource = _preprocess_extern_python(csource)
    #
    # Now there should not be any string literal left; warn if we get one
    _warn_for_string_literal(csource)
    #
    # Replace "[...]" with "[__dotdotdotarray__]"
    csource = _r_partial_array.sub('[__dotdotdotarray__]', csource)
    #
    # Replace "...}" with "__dotdotdotNUM__}".  This construction should
    # occur only at the end of enums; at the end of structs we have "...;}"
    # and at the end of vararg functions "...);".  Also replace "=...[,}]"
    # with ",__dotdotdotNUM__[,}]": this occurs in the enums too, when
    # giving an unknown value.
    matches = list(_r_partial_enum.finditer(csource))
    for number, match in enumerate(reversed(matches)):
        p = match.start()
        if csource[p] == '=':
            p2 = csource.find('...', p, match.end())
            assert p2 > p
            csource = '%s,__dotdotdot%d__ %s' % (csource[:p], number,
                                                 csource[p2+3:])
        else:
            assert csource[p:p+3] == '...'
            csource = '%s __dotdotdot%d__ %s' % (csource[:p], number,
                                                 csource[p+3:])
    # Replace "int ..." or "unsigned long int..." with "__dotdotdotint__"
    csource = _r_int_dotdotdot.sub(' __dotdotdotint__ ', csource)
    # Replace "float ..." or "double..." with "__dotdotdotfloat__"
    csource = _r_float_dotdotdot.sub(' __dotdotdotfloat__ ', csource)
    # Replace all remaining "..." with the same name, "__dotdotdot__",
    # which is declared with a typedef for the purpose of C parsing.
    csource = csource.replace('...', ' __dotdotdot__ ')
    # Finally, put back the line directives
    csource = _put_back_line_directives(csource, line_directives)
    return csource, macros


def _preprocess(enc_cnf):
    """
    Returns an encoded cnf with only Q.eq, Q.gt, Q.lt,
    Q.ge, and Q.le predicate.

    Converts every unequality into a disjunction of strict
    inequalities. For example, x != 3 would become
    x < 3 OR x > 3.

    Also converts all negated Q.ne predicates into
    equalities.
    """

    # loops through each literal in each clause
    # to construct a new, preprocessed encodedCNF

    enc_cnf = enc_cnf.copy()
    cur_enc = 1
    rev_encoding = {value: key for key, value in enc_cnf.encoding.items()}

    new_encoding = {}
    new_data = []
    for clause in enc_cnf.data:
        new_clause = []
        for lit in clause:
            if lit == 0:
                new_clause.append(lit)
                new_encoding[lit] = False
                continue
            prop = rev_encoding[abs(lit)]
            negated = lit < 0
            sign = (lit > 0) - (lit < 0)

            prop = _pred_to_binrel(prop)

            if not isinstance(prop, AppliedPredicate):
                if prop not in new_encoding:
                    new_encoding[prop] = cur_enc
                    cur_enc += 1
                lit = new_encoding[prop]
                new_clause.append(sign*lit)
                continue


            if negated and prop.function == Q.eq:
                negated = False
                prop = Q.ne(*prop.arguments)

            if prop.function == Q.ne:
                arg1, arg2 = prop.arguments
                if negated:
                    new_prop = Q.eq(arg1, arg2)
                    if new_prop not in new_encoding:
                        new_encoding[new_prop] = cur_enc
                        cur_enc += 1

                    new_enc = new_encoding[new_prop]
                    new_clause.append(new_enc)
                    continue
                else:
                    new_props = (Q.gt(arg1, arg2), Q.lt(arg1, arg2))
                    for new_prop in new_props:
                        if new_prop not in new_encoding:
                            new_encoding[new_prop] = cur_enc
                            cur_enc += 1

                        new_enc = new_encoding[new_prop]
                        new_clause.append(new_enc)
                    continue

            if prop.function == Q.eq and negated:
                assert False

            if prop not in new_encoding:
                new_encoding[prop] = cur_enc
                cur_enc += 1
            new_clause.append(new_encoding[prop]*sign)
        new_data.append(new_clause)

    assert len(new_encoding) >= cur_enc - 1

    enc_cnf = EncodedCNF(new_data, new_encoding)
    return enc_cnf


def _preprocess(expr, func=None, hint='_Integral'):
    """Prepare expr for solving by making sure that differentiation
    is done so that only func remains in unevaluated derivatives and
    (if hint does not end with _Integral) that doit is applied to all
    other derivatives. If hint is None, do not do any differentiation.
    (Currently this may cause some simple differential equations to
    fail.)

    In case func is None, an attempt will be made to autodetect the
    function to be solved for.

    >>> from sympy.solvers.deutils import _preprocess
    >>> from sympy import Derivative, Function
    >>> from sympy.abc import x, y, z
    >>> f, g = map(Function, 'fg')

    If f(x)**p == 0 and p>0 then we can solve for f(x)=0
    >>> _preprocess((f(x).diff(x)-4)**5, f(x))
    (Derivative(f(x), x) - 4, f(x))

    Apply doit to derivatives that contain more than the function
    of interest:

    >>> _preprocess(Derivative(f(x) + x, x))
    (Derivative(f(x), x) + 1, f(x))

    Do others if the differentiation variable(s) intersect with those
    of the function of interest or contain the function of interest:

    >>> _preprocess(Derivative(g(x), y, z), f(y))
    (0, f(y))
    >>> _preprocess(Derivative(f(y), z), f(y))
    (0, f(y))

    Do others if the hint does not end in '_Integral' (the default
    assumes that it does):

    >>> _preprocess(Derivative(g(x), y), f(x))
    (Derivative(g(x), y), f(x))
    >>> _preprocess(Derivative(f(x), y), f(x), hint='')
    (0, f(x))

    Do not do any derivatives if hint is None:

    >>> eq = Derivative(f(x) + 1, x) + Derivative(f(x), y)
    >>> _preprocess(eq, f(x), hint=None)
    (Derivative(f(x) + 1, x) + Derivative(f(x), y), f(x))

    If it's not clear what the function of interest is, it must be given:

    >>> eq = Derivative(f(x) + g(x), x)
    >>> _preprocess(eq, g(x))
    (Derivative(f(x), x) + Derivative(g(x), x), g(x))
    >>> try: _preprocess(eq)
    ... except ValueError: print("A ValueError was raised.")
    A ValueError was raised.

    """
    if isinstance(expr, Pow):
        # if f(x)**p=0 then f(x)=0 (p>0)
        if (expr.exp).is_positive:
            expr = expr.base
    derivs = expr.atoms(Derivative)
    if not func:
        funcs = set().union(*[d.atoms(AppliedUndef) for d in derivs])
        if len(funcs) != 1:
            raise ValueError('The function cannot be '
                'automatically detected for %s.' % expr)
        func = funcs.pop()
    fvars = set(func.args)
    if hint is None:
        return expr, func
    reps = [(d, d.doit()) for d in derivs if not hint.endswith('_Integral') or
            d.has(func) or set(d.variables) & fvars]
    eq = expr.subs(reps)
    return eq, func

