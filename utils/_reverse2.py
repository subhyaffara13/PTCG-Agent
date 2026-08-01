
def _reverse2(f):
    def reversed(is_qat, x, y):
        return f(is_qat, y, x)

    return reversed

