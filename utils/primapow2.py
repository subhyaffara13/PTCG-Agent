
def primapow2(x):
    '''
    Believe it or now, x**2 is not always the same as x*x in Python. In Fortran they
    appear to be identical. Here's a quick one-line to find an example on your system
    (well, two liner after importing numpy):
    list(filter(lambda x: x[1], [(x:=np.random.random(), x**2 - x*x != 0) for _ in range(10000)]))
    '''
    return x*x

