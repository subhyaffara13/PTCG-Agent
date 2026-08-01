
def _ischaracter(var):
    return 'typespec' in var and var['typespec'] == 'character' and \
           not isexternal(var)

