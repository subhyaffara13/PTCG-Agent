
def hasinitvalueasstring(var):
    if not hasinitvalue(var):
        return 0
    return var['='][0] in ['"', "'"]

