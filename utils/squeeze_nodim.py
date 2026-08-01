
def squeeze_nodim(li: list[int]):
    out: list[int] = []
    for i in range(len(li)):
        if li[i] != 1:
            out.append(li[i])
    return out

