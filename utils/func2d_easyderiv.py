
def func2d_easyderiv(x):
    f = 2.0*x[0]**2 + 2.0*x[0]*x[1] + 2.0*x[1]**2 - 6.0*x[0]
    df = np.zeros(2)
    df[0] = 4.0*x[0] + 2.0*x[1] - 6.0
    df[1] = 2.0*x[0] + 4.0*x[1]

    return f, df

