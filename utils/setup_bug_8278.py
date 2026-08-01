
def setup_bug_8278():
    N = 2 ** 6
    h = 1/N
    Ah1D = dia_array(([-1, 2, -1], [-1, 0, 1]), shape=(N-1, N-1))/(h**2)
    eyeN = eye_array(N - 1)
    A = (kron(eyeN, kron(eyeN, Ah1D))
         + kron(eyeN, kron(Ah1D, eyeN))
         + kron(Ah1D, kron(eyeN, eyeN)))
    b = np.random.rand((N-1)**3)
    return A, b

