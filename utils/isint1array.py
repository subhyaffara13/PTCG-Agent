
def isint1array(var):
    return isarray(var) and var.get('typespec') == 'integer' \
        and get_kind(var) == '1'

