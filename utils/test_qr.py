
def test_QR():
    A = Matrix([[1, 2], [2, 3]])
    Q, S = A.QRdecomposition()
    R = Rational
    assert Q == Matrix([
        [  5**R(-1, 2),  (R(2)/5)*(R(1)/5)**R(-1, 2)],
        [2*5**R(-1, 2), (-R(1)/5)*(R(1)/5)**R(-1, 2)]])
    assert S == Matrix([[5**R(1, 2), 8*5**R(-1, 2)], [0, (R(1)/5)**R(1, 2)]])
    assert Q*S == A
    assert Q.T * Q == eye(2)

    A = Matrix([[1, 1, 1], [1, 1, 3], [2, 3, 4]])
    Q, R = A.QRdecomposition()
    assert Q.T * Q == eye(Q.cols)
    assert R.is_upper
    assert A == Q*R

    A = Matrix([[12, 0, -51], [6, 0, 167], [-4, 0, 24]])
    Q, R = A.QRdecomposition()
    assert Q.T * Q == eye(Q.cols)
    assert R.is_upper
    assert A == Q*R

    x = Symbol('x')
    A = Matrix([x])
    Q, R = A.QRdecomposition()
    assert Q == Matrix([x / Abs(x)])
    assert R == Matrix([Abs(x)])

    A = Matrix([[x, 0], [0, x]])
    Q, R = A.QRdecomposition()
    assert Q == x / Abs(x) * Matrix([[1, 0], [0, 1]])
    assert R == Abs(x) * Matrix([[1, 0], [0, 1]])


def test_QR():
    Q_, R = qr(X)
    assert Q_.shape == R.shape == X.shape
    assert ask(Q.orthogonal(Q_))
    assert ask(Q.upper_triangular(R))


def test_qr():
    mp.dps = 15                     # used default value for dps
    lowlimit = -9                   # lower limit of matrix element value
    uplimit = 9                     # uppter limit of matrix element value
    maxm = 4                        # max matrix size
    flg = False                     # toggle to create real vs complex matrix
    zero = mpf('0.0')

    for k in xrange(0,10):
        exdps = 0
        mode = 'full'
        flg = bool(k % 2)

        # generate arbitrary matrix size (2 to maxm)
        num1 = nint(maxm*rand())
        num2 = nint(maxm*rand())
        m = int(max(num1, num2))
        n = int(min(num1, num2))

        # create matrix
        A = mp.matrix(m,n)

        # populate matrix values with arbitrary integers
        if flg:
            flg = False
            dtype = 'complex'
            for j in xrange(0,n):
                for i in xrange(0,m):
                    val = nint(lowlimit + (uplimit-lowlimit)*rand())
                    val2 = nint(lowlimit + (uplimit-lowlimit)*rand())
                    A[i,j] = mpc(val, val2)
        else:
            flg = True
            dtype = 'real'
            for j in xrange(0,n):
                for i in xrange(0,m):
                    val = nint(lowlimit + (uplimit-lowlimit)*rand())
                    A[i,j] = mpf(val)

        # perform A -> QR decomposition
        Q, R = qr(A, mode, edps = exdps)

        #print('\n\n A = \n', nstr(A, 4))
        #print('\n Q = \n', nstr(Q, 4))
        #print('\n R = \n', nstr(R, 4))
        #print('\n Q*R = \n', nstr(Q*R, 4))

        maxnorm = mpf('1.0E-11')
        n1 = norm(A - Q * R)
        #print '\n Norm of A - Q * R = ', n1
        assert n1 <= maxnorm

        if dtype == 'real':
            n1 = norm(eye(m) - Q.T * Q)
            #print ' Norm of I - Q.T * Q = ', n1
            assert n1 <= maxnorm

            n1 = norm(eye(m) - Q * Q.T)
            #print ' Norm of I - Q * Q.T = ', n1
            assert n1 <= maxnorm

        if dtype == 'complex':
            n1 = norm(eye(m) - Q.T * Q.conjugate())
            #print ' Norm of I - Q.T * Q.conjugate() = ', n1
            assert n1 <= maxnorm

            n1 = norm(eye(m) - Q.conjugate() * Q.T)
            #print ' Norm of I - Q.conjugate() * Q.T = ', n1
            assert n1 <= maxnorm

