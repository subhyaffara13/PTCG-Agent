
def true_intent_list(var):
    lst = var['intent']
    ret = []
    for intent in lst:
        try:
            f = globals()[f'isintent_{intent}']
        except KeyError:
            pass
        else:
            if f(var):
                ret.append(intent)
    return ret

