
def _get_map_slots(size, fixed_slots):
    res = list(range(size))
    pos = 0
    for i in range(size):
        if i in fixed_slots:
            continue
        res[i] = pos
        pos += 1
    return res

