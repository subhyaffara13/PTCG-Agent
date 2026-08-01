
def _powm1(x, y, *, evaluate=True):
    return Add(Pow(x, y, evaluate=evaluate), -S.One, evaluate=evaluate)

