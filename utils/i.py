
def i(a=0, /, b=0, *, c=0, d=0):
    return a + b + c + d


def i(width):
    return IntegerType.get_signless(width)

