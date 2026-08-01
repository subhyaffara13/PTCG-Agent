
def isint1(var):
    return var.get('typespec') == 'integer' \
        and get_kind(var) == '1' and not isarray(var)

