
def test_to_euler():
    q = Quaternion(w, x, y, z)
    q_normalized = q.normalize()

    seqs = ['zxy', 'zyx', 'zyz', 'zxz']
    seqs += [seq.upper() for seq in seqs]

    for seq in seqs:
        euler_from_q = q.to_euler(seq)
        q_back = simplify(Quaternion.from_euler(euler_from_q, seq))
        assert q_back == q_normalized

