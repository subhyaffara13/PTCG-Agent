
def entries(attributes, sameval=False):
    g = _entries(sorted(attributes.items(), key=lambda x: int(x[0])), sameval)
    return g

