
def iscomplexarray(var):
    return isarray(var) and \
           var.get('typespec') in ['complex', 'double complex']

