
def rubik(n):
    """Return permutations for an nxn Rubik's cube.

    Permutations returned are for rotation of each of the slice
    from the face up to the last face for each of the 3 sides (in this order):
    front, right and bottom. Hence, the first n - 1 permutations are for the
    slices from the front.
    """

    if n < 2:
        raise ValueError('dimension of cube must be > 1')

    # 1-based reference to rows and columns in Matrix
    def getr(f, i):
        return faces[f].col(n - i)

    def getl(f, i):
        return faces[f].col(i - 1)

    def getu(f, i):
        return faces[f].row(i - 1)

    def getd(f, i):
        return faces[f].row(n - i)

    def setr(f, i, s):
        faces[f][:, n - i] = Matrix(n, 1, s)

    def setl(f, i, s):
        faces[f][:, i - 1] = Matrix(n, 1, s)

    def setu(f, i, s):
        faces[f][i - 1, :] = Matrix(1, n, s)

    def setd(f, i, s):
        faces[f][n - i, :] = Matrix(1, n, s)

    # motion of a single face
    def cw(F, r=1):
        for _ in range(r):
            face = faces[F]
            rv = []
            for c in range(n):
                for r in range(n - 1, -1, -1):
                    rv.append(face[r, c])
            faces[F] = Matrix(n, n, rv)

    def ccw(F):
        cw(F, 3)

    # motion of plane i from the F side;
    # fcw(0) moves the F face, fcw(1) moves the plane
    # just behind the front face, etc...
    def fcw(i, r=1):
        for _ in range(r):
            if i == 0:
                cw(F)
            i += 1
            temp = getr(L, i)
            setr(L, i, list(getu(D, i)))
            setu(D, i, list(reversed(getl(R, i))))
            setl(R, i, list(getd(U, i)))
            setd(U, i, list(reversed(temp)))
            i -= 1

    def fccw(i):
        fcw(i, 3)

    # motion of the entire cube from the F side
    def FCW(r=1):
        for _ in range(r):
            cw(F)
            ccw(B)
            cw(U)
            t = faces[U]
            cw(L)
            faces[U] = faces[L]
            cw(D)
            faces[L] = faces[D]
            cw(R)
            faces[D] = faces[R]
            faces[R] = t

    def FCCW():
        FCW(3)

    # motion of the entire cube from the U side
    def UCW(r=1):
        for _ in range(r):
            cw(U)
            ccw(D)
            t = faces[F]
            faces[F] = faces[R]
            faces[R] = faces[B]
            faces[B] = faces[L]
            faces[L] = t

    def UCCW():
        UCW(3)

    # defining the permutations for the cube

    U, F, R, B, L, D = names = symbols('U, F, R, B, L, D')

    # the faces are represented by nxn matrices
    faces = {}
    count = 0
    for fi in range(6):
        f = []
        for a in range(n**2):
            f.append(count)
            count += 1
        faces[names[fi]] = Matrix(n, n, f)

    # this will either return the value of the current permutation
    # (show != 1) or else append the permutation to the group, g
    def perm(show=0):
        # add perm to the list of perms
        p = []
        for f in names:
            p.extend(faces[f])
        if show:
            return p
        g.append(Permutation(p))

    g = []  # container for the group's permutations
    I = list(range(6*n**2))  # the identity permutation used for checking

    # define permutations corresponding to cw rotations of the planes
    # up TO the last plane from that direction; by not including the
    # last plane, the orientation of the cube is maintained.

    # F slices
    for i in range(n - 1):
        fcw(i)
        perm()
        fccw(i)  # restore
    assert perm(1) == I

    # R slices
    # bring R to front
    UCW()
    for i in range(n - 1):
        fcw(i)
        # put it back in place
        UCCW()
        # record
        perm()
        # restore
        # bring face to front
        UCW()
        fccw(i)
    # restore
    UCCW()
    assert perm(1) == I

    # D slices
    # bring up bottom
    FCW()
    UCCW()
    FCCW()
    for i in range(n - 1):
        # turn strip
        fcw(i)
        # put bottom back on the bottom
        FCW()
        UCW()
        FCCW()
        # record
        perm()
        # restore
        # bring up bottom
        FCW()
        UCCW()
        FCCW()
        # turn strip
        fccw(i)
    # put bottom back on the bottom
    FCW()
    UCW()
    FCCW()
    assert perm(1) == I

    return g

