
def isunsigned_long_longarray(var):
    return isarray(var) and var.get('typespec') in ['integer', 'logical']\
        and get_kind(var) == '-8'

