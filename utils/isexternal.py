
def isexternal(var):
    return 'attrspec' in var and 'external' in var['attrspec']

