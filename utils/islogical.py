
def islogical(var):
    return isscalar(var) and var.get('typespec') == 'logical'

