
def _reverse3(f):
    def reversed(is_qat, x, w):
        y, z = w
        return f(is_qat, z, y, x)

    return reversed

