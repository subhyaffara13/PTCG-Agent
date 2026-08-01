
def issigned_chararray(var):
    return isarray(var) and var.get('typespec') in ['integer', 'logical']\
        and get_kind(var) == '1'

