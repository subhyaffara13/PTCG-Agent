
def isoptional(var):
    return ('attrspec' in var and 'optional' in var['attrspec'] and
            'required' not in var['attrspec']) and isintent_nothide(var)

