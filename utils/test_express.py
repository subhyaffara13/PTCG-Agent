
def test_express():
    assert express(Vector.zero, N) == Vector.zero
    assert express(S.Zero, N) is S.Zero
    assert express(A.i, C) == cos(q3)*C.i + sin(q3)*C.k
    assert express(A.j, C) == sin(q2)*sin(q3)*C.i + cos(q2)*C.j - \
        sin(q2)*cos(q3)*C.k
    assert express(A.k, C) == -sin(q3)*cos(q2)*C.i + sin(q2)*C.j + \
        cos(q2)*cos(q3)*C.k
    assert express(A.i, N) == cos(q1)*N.i + sin(q1)*N.j
    assert express(A.j, N) == -sin(q1)*N.i + cos(q1)*N.j
    assert express(A.k, N) == N.k
    assert express(A.i, A) == A.i
    assert express(A.j, A) == A.j
    assert express(A.k, A) == A.k
    assert express(A.i, B) == B.i
    assert express(A.j, B) == cos(q2)*B.j - sin(q2)*B.k
    assert express(A.k, B) == sin(q2)*B.j + cos(q2)*B.k
    assert express(A.i, C) == cos(q3)*C.i + sin(q3)*C.k
    assert express(A.j, C) == sin(q2)*sin(q3)*C.i + cos(q2)*C.j - \
        sin(q2)*cos(q3)*C.k
    assert express(A.k, C) == -sin(q3)*cos(q2)*C.i + sin(q2)*C.j + \
        cos(q2)*cos(q3)*C.k
    # Check to make sure UnitVectors get converted properly
    assert express(N.i, N) == N.i
    assert express(N.j, N) == N.j
    assert express(N.k, N) == N.k
    assert express(N.i, A) == (cos(q1)*A.i - sin(q1)*A.j)
    assert express(N.j, A) == (sin(q1)*A.i + cos(q1)*A.j)
    assert express(N.k, A) == A.k
    assert express(N.i, B) == (cos(q1)*B.i - sin(q1)*cos(q2)*B.j +
            sin(q1)*sin(q2)*B.k)
    assert express(N.j, B) == (sin(q1)*B.i + cos(q1)*cos(q2)*B.j -
            sin(q2)*cos(q1)*B.k)
    assert express(N.k, B) == (sin(q2)*B.j + cos(q2)*B.k)
    assert express(N.i, C) == (
        (cos(q1)*cos(q3) - sin(q1)*sin(q2)*sin(q3))*C.i -
        sin(q1)*cos(q2)*C.j +
        (sin(q3)*cos(q1) + sin(q1)*sin(q2)*cos(q3))*C.k)
    assert express(N.j, C) == (
        (sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1))*C.i +
        cos(q1)*cos(q2)*C.j +
        (sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3))*C.k)
    assert express(N.k, C) == (-sin(q3)*cos(q2)*C.i + sin(q2)*C.j +
            cos(q2)*cos(q3)*C.k)

    assert express(A.i, N) == (cos(q1)*N.i + sin(q1)*N.j)
    assert express(A.j, N) == (-sin(q1)*N.i + cos(q1)*N.j)
    assert express(A.k, N) == N.k
    assert express(A.i, A) == A.i
    assert express(A.j, A) == A.j
    assert express(A.k, A) == A.k
    assert express(A.i, B) == B.i
    assert express(A.j, B) == (cos(q2)*B.j - sin(q2)*B.k)
    assert express(A.k, B) == (sin(q2)*B.j + cos(q2)*B.k)
    assert express(A.i, C) == (cos(q3)*C.i + sin(q3)*C.k)
    assert express(A.j, C) == (sin(q2)*sin(q3)*C.i + cos(q2)*C.j -
            sin(q2)*cos(q3)*C.k)
    assert express(A.k, C) == (-sin(q3)*cos(q2)*C.i + sin(q2)*C.j +
            cos(q2)*cos(q3)*C.k)

    assert express(B.i, N) == (cos(q1)*N.i + sin(q1)*N.j)
    assert express(B.j, N) == (-sin(q1)*cos(q2)*N.i +
            cos(q1)*cos(q2)*N.j + sin(q2)*N.k)
    assert express(B.k, N) == (sin(q1)*sin(q2)*N.i -
            sin(q2)*cos(q1)*N.j + cos(q2)*N.k)
    assert express(B.i, A) == A.i
    assert express(B.j, A) == (cos(q2)*A.j + sin(q2)*A.k)
    assert express(B.k, A) == (-sin(q2)*A.j + cos(q2)*A.k)
    assert express(B.i, B) == B.i
    assert express(B.j, B) == B.j
    assert express(B.k, B) == B.k
    assert express(B.i, C) == (cos(q3)*C.i + sin(q3)*C.k)
    assert express(B.j, C) == C.j
    assert express(B.k, C) == (-sin(q3)*C.i + cos(q3)*C.k)

    assert express(C.i, N) == (
        (cos(q1)*cos(q3) - sin(q1)*sin(q2)*sin(q3))*N.i +
        (sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1))*N.j -
        sin(q3)*cos(q2)*N.k)
    assert express(C.j, N) == (
        -sin(q1)*cos(q2)*N.i + cos(q1)*cos(q2)*N.j + sin(q2)*N.k)
    assert express(C.k, N) == (
        (sin(q3)*cos(q1) + sin(q1)*sin(q2)*cos(q3))*N.i +
        (sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3))*N.j +
        cos(q2)*cos(q3)*N.k)
    assert express(C.i, A) == (cos(q3)*A.i + sin(q2)*sin(q3)*A.j -
            sin(q3)*cos(q2)*A.k)
    assert express(C.j, A) == (cos(q2)*A.j + sin(q2)*A.k)
    assert express(C.k, A) == (sin(q3)*A.i - sin(q2)*cos(q3)*A.j +
            cos(q2)*cos(q3)*A.k)
    assert express(C.i, B) == (cos(q3)*B.i - sin(q3)*B.k)
    assert express(C.j, B) == B.j
    assert express(C.k, B) == (sin(q3)*B.i + cos(q3)*B.k)
    assert express(C.i, C) == C.i
    assert express(C.j, C) == C.j
    assert express(C.k, C) == C.k == (C.k)

    #  Check to make sure Vectors get converted back to UnitVectors
    assert N.i == express((cos(q1)*A.i - sin(q1)*A.j), N).simplify()
    assert N.j == express((sin(q1)*A.i + cos(q1)*A.j), N).simplify()
    assert N.i == express((cos(q1)*B.i - sin(q1)*cos(q2)*B.j +
            sin(q1)*sin(q2)*B.k), N).simplify()
    assert N.j == express((sin(q1)*B.i + cos(q1)*cos(q2)*B.j -
        sin(q2)*cos(q1)*B.k), N).simplify()
    assert N.k == express((sin(q2)*B.j + cos(q2)*B.k), N).simplify()


    assert A.i == express((cos(q1)*N.i + sin(q1)*N.j), A).simplify()
    assert A.j == express((-sin(q1)*N.i + cos(q1)*N.j), A).simplify()

    assert A.j == express((cos(q2)*B.j - sin(q2)*B.k), A).simplify()
    assert A.k == express((sin(q2)*B.j + cos(q2)*B.k), A).simplify()

    assert A.i == express((cos(q3)*C.i + sin(q3)*C.k), A).simplify()
    assert A.j == express((sin(q2)*sin(q3)*C.i + cos(q2)*C.j -
            sin(q2)*cos(q3)*C.k), A).simplify()

    assert A.k == express((-sin(q3)*cos(q2)*C.i + sin(q2)*C.j +
            cos(q2)*cos(q3)*C.k), A).simplify()
    assert B.i == express((cos(q1)*N.i + sin(q1)*N.j), B).simplify()
    assert B.j == express((-sin(q1)*cos(q2)*N.i +
            cos(q1)*cos(q2)*N.j + sin(q2)*N.k), B).simplify()

    assert B.k == express((sin(q1)*sin(q2)*N.i -
            sin(q2)*cos(q1)*N.j + cos(q2)*N.k), B).simplify()

    assert B.j == express((cos(q2)*A.j + sin(q2)*A.k), B).simplify()
    assert B.k == express((-sin(q2)*A.j + cos(q2)*A.k), B).simplify()
    assert B.i == express((cos(q3)*C.i + sin(q3)*C.k), B).simplify()
    assert B.k == express((-sin(q3)*C.i + cos(q3)*C.k), B).simplify()
    assert C.i == express((cos(q3)*A.i + sin(q2)*sin(q3)*A.j -
            sin(q3)*cos(q2)*A.k), C).simplify()
    assert C.j == express((cos(q2)*A.j + sin(q2)*A.k), C).simplify()
    assert C.k == express((sin(q3)*A.i - sin(q2)*cos(q3)*A.j +
            cos(q2)*cos(q3)*A.k), C).simplify()
    assert C.i == express((cos(q3)*B.i - sin(q3)*B.k), C).simplify()
    assert C.k == express((sin(q3)*B.i + cos(q3)*B.k), C).simplify()


def test_express():
    assert express(Vector(0), N) == Vector(0)
    assert express(S.Zero, N) is S.Zero
    assert express(A.x, C) == cos(q3)*C.x + sin(q3)*C.z
    assert express(A.y, C) == sin(q2)*sin(q3)*C.x + cos(q2)*C.y - \
        sin(q2)*cos(q3)*C.z
    assert express(A.z, C) == -sin(q3)*cos(q2)*C.x + sin(q2)*C.y + \
        cos(q2)*cos(q3)*C.z
    assert express(A.x, N) == cos(q1)*N.x + sin(q1)*N.y
    assert express(A.y, N) == -sin(q1)*N.x + cos(q1)*N.y
    assert express(A.z, N) == N.z
    assert express(A.x, A) == A.x
    assert express(A.y, A) == A.y
    assert express(A.z, A) == A.z
    assert express(A.x, B) == B.x
    assert express(A.y, B) == cos(q2)*B.y - sin(q2)*B.z
    assert express(A.z, B) == sin(q2)*B.y + cos(q2)*B.z
    assert express(A.x, C) == cos(q3)*C.x + sin(q3)*C.z
    assert express(A.y, C) == sin(q2)*sin(q3)*C.x + cos(q2)*C.y - \
        sin(q2)*cos(q3)*C.z
    assert express(A.z, C) == -sin(q3)*cos(q2)*C.x + sin(q2)*C.y + \
        cos(q2)*cos(q3)*C.z
    # Check to make sure UnitVectors get converted properly
    assert express(N.x, N) == N.x
    assert express(N.y, N) == N.y
    assert express(N.z, N) == N.z
    assert express(N.x, A) == (cos(q1)*A.x - sin(q1)*A.y)
    assert express(N.y, A) == (sin(q1)*A.x + cos(q1)*A.y)
    assert express(N.z, A) == A.z
    assert express(N.x, B) == (cos(q1)*B.x - sin(q1)*cos(q2)*B.y +
            sin(q1)*sin(q2)*B.z)
    assert express(N.y, B) == (sin(q1)*B.x + cos(q1)*cos(q2)*B.y -
            sin(q2)*cos(q1)*B.z)
    assert express(N.z, B) == (sin(q2)*B.y + cos(q2)*B.z)
    assert express(N.x, C) == (
        (cos(q1)*cos(q3) - sin(q1)*sin(q2)*sin(q3))*C.x -
        sin(q1)*cos(q2)*C.y +
        (sin(q3)*cos(q1) + sin(q1)*sin(q2)*cos(q3))*C.z)
    assert express(N.y, C) == (
        (sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1))*C.x +
        cos(q1)*cos(q2)*C.y +
        (sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3))*C.z)
    assert express(N.z, C) == (-sin(q3)*cos(q2)*C.x + sin(q2)*C.y +
            cos(q2)*cos(q3)*C.z)

    assert express(A.x, N) == (cos(q1)*N.x + sin(q1)*N.y)
    assert express(A.y, N) == (-sin(q1)*N.x + cos(q1)*N.y)
    assert express(A.z, N) == N.z
    assert express(A.x, A) == A.x
    assert express(A.y, A) == A.y
    assert express(A.z, A) == A.z
    assert express(A.x, B) == B.x
    assert express(A.y, B) == (cos(q2)*B.y - sin(q2)*B.z)
    assert express(A.z, B) == (sin(q2)*B.y + cos(q2)*B.z)
    assert express(A.x, C) == (cos(q3)*C.x + sin(q3)*C.z)
    assert express(A.y, C) == (sin(q2)*sin(q3)*C.x + cos(q2)*C.y -
            sin(q2)*cos(q3)*C.z)
    assert express(A.z, C) == (-sin(q3)*cos(q2)*C.x + sin(q2)*C.y +
            cos(q2)*cos(q3)*C.z)

    assert express(B.x, N) == (cos(q1)*N.x + sin(q1)*N.y)
    assert express(B.y, N) == (-sin(q1)*cos(q2)*N.x +
            cos(q1)*cos(q2)*N.y + sin(q2)*N.z)
    assert express(B.z, N) == (sin(q1)*sin(q2)*N.x -
            sin(q2)*cos(q1)*N.y + cos(q2)*N.z)
    assert express(B.x, A) == A.x
    assert express(B.y, A) == (cos(q2)*A.y + sin(q2)*A.z)
    assert express(B.z, A) == (-sin(q2)*A.y + cos(q2)*A.z)
    assert express(B.x, B) == B.x
    assert express(B.y, B) == B.y
    assert express(B.z, B) == B.z
    assert express(B.x, C) == (cos(q3)*C.x + sin(q3)*C.z)
    assert express(B.y, C) == C.y
    assert express(B.z, C) == (-sin(q3)*C.x + cos(q3)*C.z)

    assert express(C.x, N) == (
        (cos(q1)*cos(q3) - sin(q1)*sin(q2)*sin(q3))*N.x +
        (sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1))*N.y -
        sin(q3)*cos(q2)*N.z)
    assert express(C.y, N) == (
        -sin(q1)*cos(q2)*N.x + cos(q1)*cos(q2)*N.y + sin(q2)*N.z)
    assert express(C.z, N) == (
        (sin(q3)*cos(q1) + sin(q1)*sin(q2)*cos(q3))*N.x +
        (sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3))*N.y +
        cos(q2)*cos(q3)*N.z)
    assert express(C.x, A) == (cos(q3)*A.x + sin(q2)*sin(q3)*A.y -
            sin(q3)*cos(q2)*A.z)
    assert express(C.y, A) == (cos(q2)*A.y + sin(q2)*A.z)
    assert express(C.z, A) == (sin(q3)*A.x - sin(q2)*cos(q3)*A.y +
            cos(q2)*cos(q3)*A.z)
    assert express(C.x, B) == (cos(q3)*B.x - sin(q3)*B.z)
    assert express(C.y, B) == B.y
    assert express(C.z, B) == (sin(q3)*B.x + cos(q3)*B.z)
    assert express(C.x, C) == C.x
    assert express(C.y, C) == C.y
    assert express(C.z, C) == C.z == (C.z)

    #  Check to make sure Vectors get converted back to UnitVectors
    assert N.x == express((cos(q1)*A.x - sin(q1)*A.y), N).simplify()
    assert N.y == express((sin(q1)*A.x + cos(q1)*A.y), N).simplify()
    assert N.x == express((cos(q1)*B.x - sin(q1)*cos(q2)*B.y +
            sin(q1)*sin(q2)*B.z), N).simplify()
    assert N.y == express((sin(q1)*B.x + cos(q1)*cos(q2)*B.y -
        sin(q2)*cos(q1)*B.z), N).simplify()
    assert N.z == express((sin(q2)*B.y + cos(q2)*B.z), N).simplify()

    """
    These don't really test our code, they instead test the auto simplification
    (or lack thereof) of SymPy.
    assert N.x == express((
            (cos(q1)*cos(q3)-sin(q1)*sin(q2)*sin(q3))*C.x -
            sin(q1)*cos(q2)*C.y +
            (sin(q3)*cos(q1)+sin(q1)*sin(q2)*cos(q3))*C.z), N)
    assert N.y == express((
            (sin(q1)*cos(q3) + sin(q2)*sin(q3)*cos(q1))*C.x +
            cos(q1)*cos(q2)*C.y +
            (sin(q1)*sin(q3) - sin(q2)*cos(q1)*cos(q3))*C.z), N)
    assert N.z == express((-sin(q3)*cos(q2)*C.x + sin(q2)*C.y +
            cos(q2)*cos(q3)*C.z), N)
    """

    assert A.x == express((cos(q1)*N.x + sin(q1)*N.y), A).simplify()
    assert A.y == express((-sin(q1)*N.x + cos(q1)*N.y), A).simplify()

    assert A.y == express((cos(q2)*B.y - sin(q2)*B.z), A).simplify()
    assert A.z == express((sin(q2)*B.y + cos(q2)*B.z), A).simplify()

    assert A.x == express((cos(q3)*C.x + sin(q3)*C.z), A).simplify()

    # Tripsimp messes up here too.
    #print express((sin(q2)*sin(q3)*C.x + cos(q2)*C.y -
    #        sin(q2)*cos(q3)*C.z), A)
    assert A.y == express((sin(q2)*sin(q3)*C.x + cos(q2)*C.y -
            sin(q2)*cos(q3)*C.z), A).simplify()

    assert A.z == express((-sin(q3)*cos(q2)*C.x + sin(q2)*C.y +
            cos(q2)*cos(q3)*C.z), A).simplify()
    assert B.x == express((cos(q1)*N.x + sin(q1)*N.y), B).simplify()
    assert B.y == express((-sin(q1)*cos(q2)*N.x +
            cos(q1)*cos(q2)*N.y + sin(q2)*N.z), B).simplify()

    assert B.z == express((sin(q1)*sin(q2)*N.x -
            sin(q2)*cos(q1)*N.y + cos(q2)*N.z), B).simplify()

    assert B.y == express((cos(q2)*A.y + sin(q2)*A.z), B).simplify()
    assert B.z == express((-sin(q2)*A.y + cos(q2)*A.z), B).simplify()
    assert B.x == express((cos(q3)*C.x + sin(q3)*C.z), B).simplify()
    assert B.z == express((-sin(q3)*C.x + cos(q3)*C.z), B).simplify()

    """
    assert C.x == express((
            (cos(q1)*cos(q3)-sin(q1)*sin(q2)*sin(q3))*N.x +
            (sin(q1)*cos(q3)+sin(q2)*sin(q3)*cos(q1))*N.y -
                sin(q3)*cos(q2)*N.z), C)
    assert C.y == express((
            -sin(q1)*cos(q2)*N.x + cos(q1)*cos(q2)*N.y + sin(q2)*N.z), C)
    assert C.z == express((
            (sin(q3)*cos(q1)+sin(q1)*sin(q2)*cos(q3))*N.x +
            (sin(q1)*sin(q3)-sin(q2)*cos(q1)*cos(q3))*N.y +
            cos(q2)*cos(q3)*N.z), C)
    """
    assert C.x == express((cos(q3)*A.x + sin(q2)*sin(q3)*A.y -
            sin(q3)*cos(q2)*A.z), C).simplify()
    assert C.y == express((cos(q2)*A.y + sin(q2)*A.z), C).simplify()
    assert C.z == express((sin(q3)*A.x - sin(q2)*cos(q3)*A.y +
            cos(q2)*cos(q3)*A.z), C).simplify()
    assert C.x == express((cos(q3)*B.x - sin(q3)*B.z), C).simplify()
    assert C.z == express((sin(q3)*B.x + cos(q3)*B.z), C).simplify()

