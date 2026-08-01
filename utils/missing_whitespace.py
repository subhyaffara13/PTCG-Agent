
def missing_whitespace(logical_line, tokens):
    r"""Surround operators with the correct amount of whitespace.

    - Always surround these binary operators with a single space on
      either side: assignment (=), augmented assignment (+=, -= etc.),
      comparisons (==, <, >, !=, <=, >=, in, not in, is, is not),
      Booleans (and, or, not).

    - Each comma, semicolon or colon should be followed by whitespace.

    - If operators with different priorities are used, consider adding
      whitespace around the operators with the lowest priorities.

    Okay: i = i + 1
    Okay: submitted += 1
    Okay: x = x * 2 - 1
    Okay: hypot2 = x * x + y * y
    Okay: c = (a + b) * (a - b)
    Okay: foo(bar, key='word', *args, **kwargs)
    Okay: alpha[:-i]
    Okay: [a, b]
    Okay: (3,)
    Okay: a[3,] = 1
    Okay: a[1:4]
    Okay: a[:4]
    Okay: a[1:]
    Okay: a[1:4:2]

    E225: i=i+1
    E225: submitted +=1
    E225: x = x /2 - 1
    E225: z = x **y
    E225: z = 1and 1
    E226: c = (a+b) * (a-b)
    E226: hypot2 = x*x + y*y
    E227: c = a|b
    E228: msg = fmt%(errno, errmsg)
    E231: ['a','b']
    E231: foo(bar,baz)
    E231: [{'a':'b'}]
    """
    need_space = False
    prev_type = tokenize.OP
    prev_text = prev_end = None
    operator_types = (tokenize.OP, tokenize.NAME)
    brace_stack = []
    for token_type, text, start, end, line in tokens:
        if token_type == tokenize.OP and text in {'[', '(', '{'}:
            brace_stack.append(text)
        elif token_type == FSTRING_START:  # pragma: >=3.12 cover
            brace_stack.append('f')
        elif token_type == TSTRING_START:  # pragma: >=3.14 cover
            brace_stack.append('t')
        elif token_type == tokenize.NAME and text == 'lambda':
            brace_stack.append('l')
        elif brace_stack:
            if token_type == tokenize.OP and text in {']', ')', '}'}:
                brace_stack.pop()
            elif token_type == FSTRING_END:  # pragma: >=3.12 cover
                brace_stack.pop()
            elif token_type == TSTRING_END:  # pragma: >=3.14 cover
                brace_stack.pop()
            elif (
                    brace_stack[-1] == 'l' and
                    token_type == tokenize.OP and
                    text == ':'
            ):
                brace_stack.pop()

        if token_type in SKIP_COMMENTS:
            continue

        if token_type == tokenize.OP and text in {',', ';', ':'}:
            next_char = line[end[1]:end[1] + 1]
            if next_char not in WHITESPACE and next_char not in '\r\n':
                # slice
                if text == ':' and brace_stack[-1:] == ['[']:
                    pass
                # 3.12+ fstring format specifier
                elif text == ':' and brace_stack[-2:] == ['f', '{']:  # pragma: >=3.12 cover  # noqa: E501
                    pass
                # 3.14+ tstring format specifier
                elif text == ':' and brace_stack[-2:] == ['t', '{']:  # pragma: >=3.14 cover  # noqa: E501
                    pass
                # tuple (and list for some reason?)
                elif text == ',' and next_char in ')]':
                    pass
                else:
                    yield start, f'E231 missing whitespace after {text!r}'

        if need_space:
            if start != prev_end:
                # Found a (probably) needed space
                if need_space is not True and not need_space[1]:
                    yield (need_space[0],
                           "E225 missing whitespace around operator")
                need_space = False
            elif (
                    # def f(a, /, b):
                    #           ^
                    # def f(a, b, /):
                    #              ^
                    # f = lambda a, /:
                    #                ^
                    prev_text == '/' and text in {',', ')', ':'} or
                    # def f(a, b, /):
                    #               ^
                    prev_text == ')' and text == ':'
            ):
                # Tolerate the "/" operator in function definition
                # For more info see PEP570
                pass
            else:
                if need_space is True or need_space[1]:
                    # A needed trailing space was not found
                    yield prev_end, "E225 missing whitespace around operator"
                elif prev_text != '**':
                    code, optype = 'E226', 'arithmetic'
                    if prev_text == '%':
                        code, optype = 'E228', 'modulo'
                    elif prev_text not in ARITHMETIC_OP:
                        code, optype = 'E227', 'bitwise or shift'
                    yield (need_space[0], "%s missing whitespace "
                           "around %s operator" % (code, optype))
                need_space = False
        elif token_type in operator_types and prev_end is not None:
            if (
                    text == '=' and (
                        # allow lambda default args: lambda x=None: None
                        brace_stack[-1:] == ['l'] or
                        # allow keyword args or defaults: foo(bar=None).
                        brace_stack[-1:] == ['('] or
                        # allow python 3.8 fstring repr specifier
                        brace_stack[-2:] == ['f', '{'] or
                        # allow python 3.8 fstring repr specifier
                        brace_stack[-2:] == ['t', '{']
                    )
            ):
                pass
            elif text in WS_NEEDED_OPERATORS:
                need_space = True
            elif text in UNARY_OPERATORS:
                # Check if the operator is used as a binary operator
                # Allow unary operators: -123, -x, +1.
                # Allow argument unpacking: foo(*args, **kwargs).
                if prev_type == tokenize.OP and prev_text in '}])' or (
                    prev_type != tokenize.OP and
                    prev_text not in KEYWORDS and
                    not keyword.issoftkeyword(prev_text)
                ):
                    need_space = None
            elif text in WS_OPTIONAL_OPERATORS:
                need_space = None

            if need_space is None:
                # Surrounding space is optional, but ensure that
                # trailing space matches opening space
                need_space = (prev_end, start != prev_end)
            elif need_space and start == prev_end:
                # A needed opening space was not found
                yield prev_end, "E225 missing whitespace around operator"
                need_space = False
        prev_type = token_type
        prev_text = text
        prev_end = end

