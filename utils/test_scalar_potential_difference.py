
def test_scalar_potential_difference():
    point1 = C.origin.locate_new('P1', 1*i + 2*j + 3*k)
    point2 = C.origin.locate_new('P2', 4*i + 5*j + 6*k)
    genericpointC = C.origin.locate_new('RP', x*i + y*j + z*k)
    genericpointP = P.origin.locate_new('PP', P.x*P.i + P.y*P.j + P.z*P.k)
    assert scalar_potential_difference(S.Zero, C, point1, point2) == 0
    assert (scalar_potential_difference(scalar_field, C, C.origin,
                                        genericpointC) ==
            scalar_field)
    assert (scalar_potential_difference(grad_field, C, C.origin,
                                        genericpointC) ==
            scalar_field)
    assert scalar_potential_difference(grad_field, C, point1, point2) == 948
    assert (scalar_potential_difference(y*z*i + x*z*j +
                                        x*y*k, C, point1,
                                        genericpointC) ==
            x*y*z - 6)
    potential_diff_P = (2*P.z*(P.x*sin(q) + P.y*cos(q))*
                        (P.x*cos(q) - P.y*sin(q))**2)
    assert (scalar_potential_difference(grad_field, P, P.origin,
                                        genericpointP).simplify() ==
            potential_diff_P.simplify())


def test_scalar_potential_difference():
    origin = Point('O')
    point1 = origin.locatenew('P1', 1*R.x + 2*R.y + 3*R.z)
    point2 = origin.locatenew('P2', 4*R.x + 5*R.y + 6*R.z)
    genericpointR = origin.locatenew('RP', R[0]*R.x + R[1]*R.y + R[2]*R.z)
    genericpointP = origin.locatenew('PP', P[0]*P.x + P[1]*P.y + P[2]*P.z)
    assert scalar_potential_difference(S.Zero, R, point1, point2, \
                                       origin) == 0
    assert scalar_potential_difference(scalar_field, R, origin, \
                                       genericpointR, origin) == \
                                       scalar_field
    assert scalar_potential_difference(grad_field, R, origin, \
                                       genericpointR, origin) == \
                                       scalar_field
    assert scalar_potential_difference(grad_field, R, point1, point2,
                                       origin) == 948
    assert scalar_potential_difference(R[1]*R[2]*R.x + R[0]*R[2]*R.y + \
                                       R[0]*R[1]*R.z, R, point1,
                                       genericpointR, origin) == \
                                       R[0]*R[1]*R[2] - 6
    potential_diff_P = 2*P[2]*(P[0]*sin(q) + P[1]*cos(q))*\
                       (P[0]*cos(q) - P[1]*sin(q))**2
    assert scalar_potential_difference(grad_field, P, origin, \
                                       genericpointP, \
                                       origin).simplify() == \
                                       potential_diff_P

