
def _flatten_group(group):
    ret = []
    if isinstance(group, (tuple, list)):
        for item in group:
            ret.extend(_flatten_group(item))
    elif hasattr(group, "enum"):
        ret.extend(_flatten_group(group.enum))
    else:
        ret.append(group)
    return ret

