
def eqmask(m1, m2):
    if m1 is nomask:
        return m2 is nomask
    if m2 is nomask:
        return m1 is nomask
    return (m1 == m2).all()

