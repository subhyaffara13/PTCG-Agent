
def isvariable(var):
    # heuristic to find public/private declarations of filtered subroutines
    if len(var) == 1 and 'attrspec' in var and \
            var['attrspec'][0] in ('public', 'private'):
        is_var = False
    else:
        is_var = True
    return is_var

