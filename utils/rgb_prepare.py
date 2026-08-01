
def rgb_prepare(triple):
    ret = []
    for ch in triple:
        ch = round(ch, 3)

        if ch < -0.0001 or ch > 1.0001:
            raise Exception(f"Illegal RGB value {ch:f}")

        if ch < 0:
            ch = 0
        if ch > 1:
            ch = 1

        # Fix for Python 3 which by default rounds 4.5 down to 4.0
        # instead of Python 2 which is rounded to 5.0 which caused
        # a couple off by one errors in the tests. Tests now all pass
        # in Python 2 and Python 3
        ret.append(int(round(ch * 255 + 0.001, 0)))

    return ret

