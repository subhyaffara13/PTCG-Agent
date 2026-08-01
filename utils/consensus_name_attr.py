
def consensus_name_attr(objs):
    name = objs[0].name
    for obj in objs[1:]:
        try:
            if obj.name != name:
                name = None
                break
        except ValueError:
            name = None
            break
    return name

