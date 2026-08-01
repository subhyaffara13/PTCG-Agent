
def getstrlength(var):
    if isstringfunction(var):
        if 'result' in var:
            a = var['result']
        else:
            a = var['name']
        if a in var['vars']:
            return getstrlength(var['vars'][a])
        else:
            errmess(f'getstrlength: function {a} has no return value?!\n')
    if not isstring(var):
        errmess(
            f'getstrlength: expected a signature of a string but got: {repr(var)}\n')
    len = '1'
    if 'charselector' in var:
        a = var['charselector']
        if '*' in a:
            len = a['*']
        elif 'len' in a:
            len = f2cexpr(a['len'])
    if re.match(r'\(\s*(\*|:)\s*\)', len) or re.match(r'(\*|:)', len):
        if isintent_hide(var):
            errmess(f'getstrlength:intent(hide): expected a string with defined length '
                    f'but got: {var!r}\n')
        len = '-1'
    return len

