
def getrestdoc(rout):
    if 'f2pymultilines' not in rout:
        return None
    k = None
    if rout['block'] == 'python module':
        k = rout['block'], rout['name']
    return rout['f2pymultilines'].get(k, None)

