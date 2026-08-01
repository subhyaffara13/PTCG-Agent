
def compare_equal_outs_and_grads(test, m1, m2, inps):
    r1, g1 = outs_and_grads(m1, inps, inps)
    r2, g2 = outs_and_grads(m2, inps, inps)
    test.assertEqual(r1, r2)
    test.assertEqual(g1, g2)

