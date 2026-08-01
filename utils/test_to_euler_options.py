
def test_to_euler_options():
    def test_one_case(q):
        angles1 = Matrix(q.to_euler(seq, True, True))
        angles2 = Matrix(q.to_euler(seq, False, False))
        angle_errors = simplify(angles1-angles2).evalf()
        for angle_error in angle_errors:
            # forcing angles to set {-pi, pi}
            angle_error = (angle_error + pi) % (2 * pi) - pi
            assert angle_error < 10e-7

    for xyz in ('xyz', 'XYZ'):
        for seq_tuple in permutations(xyz):
            for symmetric in (True, False):
                if symmetric:
                    seq = ''.join([seq_tuple[0], seq_tuple[1], seq_tuple[0]])
                else:
                    seq = ''.join(seq_tuple)

                for elements in product([-1, 0, 1], repeat=4):
                    q = Quaternion(*elements)
                    if not q.is_zero_quaternion():
                        test_one_case(q)

