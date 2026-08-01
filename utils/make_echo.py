
def make_echo(sound, samples_per_second, mydebug=True):
    """returns a sound which is echoed of the last one."""

    echo_length = 3.5

    a1 = pg.sndarray.array(sound)
    if mydebug:
        print(f"SHAPE1: {a1.shape}")

    length = a1.shape[0]

    # myarr = zeros(length+12000)
    myarr = zeros(a1.shape, int32)

    if len(a1.shape) > 1:
        # mult = a1.shape[1]
        size = (a1.shape[0] + int(echo_length * a1.shape[0]), a1.shape[1])
        # size = (a1.shape[0] + int(a1.shape[0] + (echo_length * 3000)), a1.shape[1])
    else:
        # mult = 1
        size = (a1.shape[0] + int(echo_length * a1.shape[0]),)
        # size = (a1.shape[0] + int(a1.shape[0] + (echo_length * 3000)),)

    if mydebug:
        print(int(echo_length * a1.shape[0]))
    myarr = zeros(size, int32)

    if mydebug:
        print(f"size {size}")
        print(myarr.shape)
    myarr[:length] = a1
    # print(myarr[3000:length+3000])
    # print(a1 >> 1)
    # print("a1.shape %s" % (a1.shape,))
    # c = myarr[3000:length+(3000*mult)]
    # print("c.shape %s" % (c.shape,))

    incr = int(samples_per_second / echo_length)
    gap = length

    myarr[incr : gap + incr] += a1 >> 1
    myarr[incr * 2 : gap + (incr * 2)] += a1 >> 2
    myarr[incr * 3 : gap + (incr * 3)] += a1 >> 3
    myarr[incr * 4 : gap + (incr * 4)] += a1 >> 4

    if mydebug:
        print(f"SHAPE2: {myarr.shape}")

    sound2 = pg.sndarray.make_sound(myarr.astype(int16))

    return sound2

