
def test_coordinate_vars():
    """
    Tests the coordinate variables functionality with respect to
    reorientation of coordinate systems.
    """
    A = CoordSys3D('A')
    # Note that the name given on the lhs is different from A.x._name
    assert BaseScalar(0, A, 'A_x', r'\mathbf{{x}_{A}}') == A.x
    assert BaseScalar(1, A, 'A_y', r'\mathbf{{y}_{A}}') == A.y
    assert BaseScalar(2, A, 'A_z', r'\mathbf{{z}_{A}}') == A.z
    assert BaseScalar(0, A, 'A_x', r'\mathbf{{x}_{A}}').__hash__() == A.x.__hash__()
    assert isinstance(A.x, BaseScalar) and \
           isinstance(A.y, BaseScalar) and \
           isinstance(A.z, BaseScalar)
    assert A.x*A.y == A.y*A.x
    assert A.scalar_map(A) == {A.x: A.x, A.y: A.y, A.z: A.z}
    assert A.x.system == A
    assert A.x.diff(A.x) == 1
    B = A.orient_new_axis('B', q, A.k)
    assert B.scalar_map(A) == {B.z: A.z, B.y: -A.x*sin(q) + A.y*cos(q),
                                 B.x: A.x*cos(q) + A.y*sin(q)}
    assert A.scalar_map(B) == {A.x: B.x*cos(q) - B.y*sin(q),
                                 A.y: B.x*sin(q) + B.y*cos(q), A.z: B.z}
    assert express(B.x, A, variables=True) == A.x*cos(q) + A.y*sin(q)
    assert express(B.y, A, variables=True) == -A.x*sin(q) + A.y*cos(q)
    assert express(B.z, A, variables=True) == A.z
    assert expand(express(B.x*B.y*B.z, A, variables=True)) == \
           expand(A.z*(-A.x*sin(q) + A.y*cos(q))*(A.x*cos(q) + A.y*sin(q)))
    assert express(B.x*B.i + B.y*B.j + B.z*B.k, A) == \
           (B.x*cos(q) - B.y*sin(q))*A.i + (B.x*sin(q) + \
           B.y*cos(q))*A.j + B.z*A.k
    assert simplify(express(B.x*B.i + B.y*B.j + B.z*B.k, A, \
                            variables=True)) == \
           A.x*A.i + A.y*A.j + A.z*A.k
    assert express(A.x*A.i + A.y*A.j + A.z*A.k, B) == \
           (A.x*cos(q) + A.y*sin(q))*B.i + \
           (-A.x*sin(q) + A.y*cos(q))*B.j + A.z*B.k
    assert simplify(express(A.x*A.i + A.y*A.j + A.z*A.k, B, \
                            variables=True)) == \
           B.x*B.i + B.y*B.j + B.z*B.k
    N = B.orient_new_axis('N', -q, B.k)
    assert N.scalar_map(A) == \
           {N.x: A.x, N.z: A.z, N.y: A.y}
    C = A.orient_new_axis('C', q, A.i + A.j + A.k)
    mapping = A.scalar_map(C)
    assert mapping[A.x].equals(C.x*(2*cos(q) + 1)/3 +
                            C.y*(-2*sin(q + pi/6) + 1)/3 +
                            C.z*(-2*cos(q + pi/3) + 1)/3)
    assert mapping[A.y].equals(C.x*(-2*cos(q + pi/3) + 1)/3 +
                            C.y*(2*cos(q) + 1)/3 +
                            C.z*(-2*sin(q + pi/6) + 1)/3)
    assert mapping[A.z].equals(C.x*(-2*sin(q + pi/6) + 1)/3 +
                            C.y*(-2*cos(q + pi/3) + 1)/3 +
                            C.z*(2*cos(q) + 1)/3)
    D = A.locate_new('D', a*A.i + b*A.j + c*A.k)
    assert D.scalar_map(A) == {D.z: A.z - c, D.x: A.x - a, D.y: A.y - b}
    E = A.orient_new_axis('E', a, A.k, a*A.i + b*A.j + c*A.k)
    assert A.scalar_map(E) == {A.z: E.z + c,
                               A.x: E.x*cos(a) - E.y*sin(a) + a,
                               A.y: E.x*sin(a) + E.y*cos(a) + b}
    assert E.scalar_map(A) == {E.x: (A.x - a)*cos(a) + (A.y - b)*sin(a),
                               E.y: (-A.x + a)*sin(a) + (A.y - b)*cos(a),
                               E.z: A.z - c}
    F = A.locate_new('F', Vector.zero)
    assert A.scalar_map(F) == {A.z: F.z, A.x: F.x, A.y: F.y}


def test_coordinate_vars():
    """Tests the coordinate variables functionality"""
    A = ReferenceFrame('A')
    assert CoordinateSym('Ax', A, 0) == A[0]
    assert CoordinateSym('Ax', A, 1) == A[1]
    assert CoordinateSym('Ax', A, 2) == A[2]
    raises(ValueError, lambda: CoordinateSym('Ax', A, 3))
    q = dynamicsymbols('q')
    qd = dynamicsymbols('q', 1)
    assert isinstance(A[0], CoordinateSym) and \
           isinstance(A[0], CoordinateSym) and \
           isinstance(A[0], CoordinateSym)
    assert A.variable_map(A) == {A[0]:A[0], A[1]:A[1], A[2]:A[2]}
    assert A[0].frame == A
    B = A.orientnew('B', 'Axis', [q, A.z])
    assert B.variable_map(A) == {B[2]: A[2], B[1]: -A[0]*sin(q) + A[1]*cos(q),
                                 B[0]: A[0]*cos(q) + A[1]*sin(q)}
    assert A.variable_map(B) == {A[0]: B[0]*cos(q) - B[1]*sin(q),
                                 A[1]: B[0]*sin(q) + B[1]*cos(q), A[2]: B[2]}
    assert time_derivative(B[0], A) == -A[0]*sin(q)*qd + A[1]*cos(q)*qd
    assert time_derivative(B[1], A) == -A[0]*cos(q)*qd - A[1]*sin(q)*qd
    assert time_derivative(B[2], A) == 0
    assert express(B[0], A, variables=True) == A[0]*cos(q) + A[1]*sin(q)
    assert express(B[1], A, variables=True) == -A[0]*sin(q) + A[1]*cos(q)
    assert express(B[2], A, variables=True) == A[2]
    assert time_derivative(A[0]*A.x + A[1]*A.y + A[2]*A.z, B) == A[1]*qd*A.x - A[0]*qd*A.y
    assert time_derivative(B[0]*B.x + B[1]*B.y + B[2]*B.z, A) == - B[1]*qd*B.x + B[0]*qd*B.y
    assert express(B[0]*B[1]*B[2], A, variables=True) == \
           A[2]*(-A[0]*sin(q) + A[1]*cos(q))*(A[0]*cos(q) + A[1]*sin(q))
    assert (time_derivative(B[0]*B[1]*B[2], A) -
            (A[2]*(-A[0]**2*cos(2*q) -
             2*A[0]*A[1]*sin(2*q) +
             A[1]**2*cos(2*q))*qd)).trigsimp() == 0
    assert express(B[0]*B.x + B[1]*B.y + B[2]*B.z, A) == \
           (B[0]*cos(q) - B[1]*sin(q))*A.x + (B[0]*sin(q) + \
           B[1]*cos(q))*A.y + B[2]*A.z
    assert express(B[0]*B.x + B[1]*B.y + B[2]*B.z, A,
                   variables=True).simplify() == A[0]*A.x + A[1]*A.y + A[2]*A.z
    assert express(A[0]*A.x + A[1]*A.y + A[2]*A.z, B) == \
           (A[0]*cos(q) + A[1]*sin(q))*B.x + \
           (-A[0]*sin(q) + A[1]*cos(q))*B.y + A[2]*B.z
    assert express(A[0]*A.x + A[1]*A.y + A[2]*A.z, B,
                   variables=True).simplify() == B[0]*B.x + B[1]*B.y + B[2]*B.z
    N = B.orientnew('N', 'Axis', [-q, B.z])
    assert ({k: v.simplify() for k, v in N.variable_map(A).items()} ==
            {N[0]: A[0], N[2]: A[2], N[1]: A[1]})
    C = A.orientnew('C', 'Axis', [q, A.x + A.y + A.z])
    mapping = A.variable_map(C)
    assert trigsimp(mapping[A[0]]) == (2*C[0]*cos(q)/3 + C[0]/3 -
                                       2*C[1]*sin(q + pi/6)/3 +
                                       C[1]/3 - 2*C[2]*cos(q + pi/3)/3 +
                                       C[2]/3)
    assert trigsimp(mapping[A[1]]) == -2*C[0]*cos(q + pi/3)/3 + \
           C[0]/3 + 2*C[1]*cos(q)/3 + C[1]/3 - 2*C[2]*sin(q + pi/6)/3 + C[2]/3
    assert trigsimp(mapping[A[2]]) == -2*C[0]*sin(q + pi/6)/3 + C[0]/3 - \
           2*C[1]*cos(q + pi/3)/3 + C[1]/3 + 2*C[2]*cos(q)/3 + C[2]/3

