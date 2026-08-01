
def scale_value_list(flist):
    v_min, v_max = min(flist), max(flist)
    v_len = v_max - v_min
    return [scale_value(f, v_min, v_len) for f in flist]

