
def _generate_body(interframe=False):
    N = ReferenceFrame('N')
    A = ReferenceFrame('A')
    P = RigidBody('P', frame=N)
    C = RigidBody('C', frame=A)
    if interframe:
        Pint, Cint = ReferenceFrame('P_int'), ReferenceFrame('C_int')
        Pint.orient_axis(N, N.x, pi)
        Cint.orient_axis(A, A.y, -pi / 2)
        return N, A, P, C, Pint, Cint
    return N, A, P, C

