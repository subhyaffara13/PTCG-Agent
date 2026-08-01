
def buildimplicitrules(block):
    setmesstext(block)
    implicitrules = defaultimplicitrules
    attrrules = {}
    if 'implicit' in block:
        if block['implicit'] is None:
            implicitrules = None
            if verbose > 1:
                outmess(
                    f"buildimplicitrules: no implicit rules for routine {repr(block['name'])}.\n")
        else:
            for k in list(block['implicit'].keys()):
                if block['implicit'][k].get('typespec') not in ['static', 'automatic']:
                    implicitrules[k] = block['implicit'][k]
                else:
                    attrrules[k] = block['implicit'][k]['typespec']
    return implicitrules, attrrules

