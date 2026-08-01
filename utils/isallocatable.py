
def isallocatable(var):
    return 'attrspec' in var and 'allocatable' in var['attrspec']

