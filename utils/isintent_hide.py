
def isintent_hide(var):
    return ('intent' in var and ('hide' in var['intent'] or
            ('out' in var['intent'] and 'in' not in var['intent'] and
                (not l_or(isintent_inout, isintent_inplace)(var)))))

