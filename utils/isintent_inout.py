
def isintent_inout(var):
    return ('intent' in var and ('inout' in var['intent'] or
            'outin' in var['intent']) and 'in' not in var['intent'] and
            'hide' not in var['intent'] and 'inplace' not in var['intent'])

