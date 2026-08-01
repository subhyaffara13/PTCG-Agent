
def _commastring(astr):
    startindex = 0
    result = []
    islist = False
    while startindex < len(astr):
        mo = format_re.match(astr, pos=startindex)
        try:
            (order1, repeats, order2, dtype) = mo.groups()
        except (TypeError, AttributeError):
            raise ValueError(
                f'format number {len(result) + 1} of "{astr}" is not recognized'
                ) from None
        startindex = mo.end()
        # Separator or ending padding
        if startindex < len(astr):
            if space_re.match(astr, pos=startindex):
                startindex = len(astr)
            else:
                mo = sep_re.match(astr, pos=startindex)
                if not mo:
                    raise ValueError(
                        f'format number {len(result) + 1} of "{astr}" '
                        'is not recognized')
                startindex = mo.end()
                islist = True

        if order2 == '':
            order = order1
        elif order1 == '':
            order = order2
        else:
            order1 = _convorder.get(order1, order1)
            order2 = _convorder.get(order2, order2)
            if (order1 != order2):
                raise ValueError(
                    f'inconsistent byte-order specification {order1} and {order2}')
            order = order1

        if order in ('|', '=', _nbo):
            order = ''
        dtype = order + dtype
        if repeats == '':
            newitem = dtype
        else:
            if (repeats[0] == "(" and repeats[-1] == ")"
                    and repeats[1:-1].strip() != ""
                    and "," not in repeats):
                warnings.warn(
                    'Passing in a parenthesized single number for repeats '
                    'is deprecated; pass either a single number or indicate '
                    'a tuple with a comma, like "(2,)".', DeprecationWarning,
                    stacklevel=2)
            newitem = (dtype, ast.literal_eval(repeats))

        result.append(newitem)

    return result if islist else result[0]

