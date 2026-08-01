
def markouterparen(line):
    l = ''
    f = 0
    for c in line:
        if c == '(':
            f = f + 1
            if f == 1:
                l = l + '@(@'
                continue
        elif c == ')':
            f = f - 1
            if f == 0:
                l = l + '@)@'
                continue
        l = l + c
    return l

