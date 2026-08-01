
def fv(t, x, omega):
    dxdt = [omega[0]*x[1], -omega[1]*x[0]]
    return dxdt

