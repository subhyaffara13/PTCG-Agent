
def unpack_item(item):
    tp = type(item.value)
    if tp == dict:
        newitem = {}
        for key, value in item.value.items():
            newitem[key] = unpack_item(value)
    elif tp == list:
        newitem = [None] * len(item.value)
        for i in range(len(item.value)):
            newitem[i] = unpack_item(item.value[i])
        if item.type == "proceduretype":
            newitem = tuple(newitem)
    else:
        newitem = item.value
    return newitem

