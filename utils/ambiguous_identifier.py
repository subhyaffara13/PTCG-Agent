
def ambiguous_identifier(logical_line, tokens):
    r"""Never use the characters 'l', 'O', or 'I' as variable names.

    In some fonts, these characters are indistinguishable from the
    numerals one and zero. When tempted to use 'l', use 'L' instead.

    Okay: L = 0
    Okay: o = 123
    Okay: i = 42
    E741: l = 0
    E741: O = 123
    E741: I = 42

    Variables can be bound in several other contexts, including class
    and function definitions, lambda functions, 'global' and 'nonlocal'
    statements, exception handlers, and 'with' and 'for' statements.
    In addition, we have a special handling for function parameters.

    Okay: except AttributeError as o:
    Okay: with lock as L:
    Okay: foo(l=12)
    Okay: foo(l=I)
    Okay: for a in foo(l=12):
    Okay: lambda arg: arg * l
    Okay: lambda a=l[I:5]: None
    Okay: lambda x=a.I: None
    Okay: if l >= 12:
    E741: except AttributeError as O:
    E741: with lock as l:
    E741: global I
    E741: nonlocal l
    E741: def foo(l):
    E741: def foo(l=12):
    E741: l = foo(l=12)
    E741: for l in range(10):
    E741: [l for l in lines if l]
    E741: lambda l: None
    E741: lambda a=x[1:5], l: None
    E741: lambda **l:
    E741: def f(**l):
    E742: class I(object):
    E743: def l(x):
    """
    func_depth = None  # set to brace depth if 'def' or 'lambda' is found
    seen_colon = False  # set to true if we're done with function parameters
    brace_depth = 0
    idents_to_avoid = ('l', 'O', 'I')
    prev_type, prev_text, prev_start, prev_end, __ = tokens[0]
    for index in range(1, len(tokens)):
        token_type, text, start, end, line = tokens[index]
        ident = pos = None
        # find function definitions
        if prev_text in {'def', 'lambda'}:
            func_depth = brace_depth
            seen_colon = False
        elif (
                func_depth is not None and
                text == ':' and
                brace_depth == func_depth
        ):
            seen_colon = True
        # update parameter parentheses level
        if text in '([{':
            brace_depth += 1
        elif text in ')]}':
            brace_depth -= 1
        # identifiers on the lhs of an assignment operator
        if text == ':=' or (text == '=' and brace_depth == 0):
            if prev_text in idents_to_avoid:
                ident = prev_text
                pos = prev_start
        # identifiers bound to values with 'as', 'for',
        # 'global', or 'nonlocal'
        if prev_text in ('as', 'for', 'global', 'nonlocal'):
            if text in idents_to_avoid:
                ident = text
                pos = start
        # function / lambda parameter definitions
        if (
                func_depth is not None and
                not seen_colon and
                index < len(tokens) - 1 and tokens[index + 1][1] in ':,=)' and
                prev_text in {'lambda', ',', '*', '**', '('} and
                text in idents_to_avoid
        ):
            ident = text
            pos = start
        if prev_text == 'class':
            if text in idents_to_avoid:
                yield start, "E742 ambiguous class definition '%s'" % text
        if prev_text == 'def':
            if text in idents_to_avoid:
                yield start, "E743 ambiguous function definition '%s'" % text
        if ident:
            yield pos, "E741 ambiguous variable name '%s'" % ident
        prev_text = text
        prev_start = start

