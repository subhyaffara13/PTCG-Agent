
def _num_fromflags(flaglist):
    num = 0
    for val in flaglist:
        num += mu._flagdict[val]
    return num

