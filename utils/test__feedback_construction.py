
def test_Feedback_construction():
    tf1 = TransferFunction(1, s**2 + 2*zeta*wn*s + wn**2, s)
    tf2 = TransferFunction(k, 1, s)
    tf3 = TransferFunction(a2*p - s, a2*s + p, s)
    tf4 = TransferFunction(a0*p + p**a1 - s, p, p)
    tf5 = TransferFunction(a1*s**2 + a2*s - a0, s + a0, s)
    tf6 = TransferFunction(s - p, p + s, p)

    f1 = Feedback(TransferFunction(1, 1, s), tf1*tf2*tf3)
    assert f1.args == (TransferFunction(1, 1, s), Series(tf1, tf2, tf3), -1)
    assert f1.sys1 == TransferFunction(1, 1, s)
    assert f1.sys2 == Series(tf1, tf2, tf3)
    assert f1.var == s

    f2 = Feedback(tf1, tf2*tf3)
    assert f2.args == (tf1, Series(tf2, tf3), -1)
    assert f2.sys1 == tf1
    assert f2.sys2 == Series(tf2, tf3)
    assert f2.var == s

    f3 = Feedback(tf1*tf2, tf5)
    assert f3.args == (Series(tf1, tf2), tf5, -1)
    assert f3.sys1 == Series(tf1, tf2)

    f4 = Feedback(tf4, tf6)
    assert f4.args == (tf4, tf6, -1)
    assert f4.sys1 == tf4
    assert f4.var == p

    f5 = Feedback(tf5, TransferFunction(1, 1, s))
    assert f5.args == (tf5, TransferFunction(1, 1, s), -1)
    assert f5.var == s
    assert f5 == Feedback(tf5)  # When sys2 is not passed explicitly, it is assumed to be unit tf.

    f6 = Feedback(TransferFunction(1, 1, p), tf4)
    assert f6.args == (TransferFunction(1, 1, p), tf4, -1)
    assert f6.var == p

    f7 = -Feedback(tf4*tf6, TransferFunction(1, 1, p))
    assert f7.args == (Series(TransferFunction(-1, 1, p), Series(tf4, tf6)), -TransferFunction(1, 1, p), -1)
    assert f7.sys1 == Series(TransferFunction(-1, 1, p), Series(tf4, tf6))

    # denominator can't be a Parallel instance
    raises(TypeError, lambda: Feedback(tf1, tf2 + tf3))
    raises(TypeError, lambda: Feedback(tf1, Matrix([1, 2, 3])))
    raises(TypeError, lambda: Feedback(TransferFunction(1, 1, s), s - 1))
    raises(TypeError, lambda: Feedback(1, 1))
    # raises(ValueError, lambda: Feedback(TransferFunction(1, 1, s), TransferFunction(1, 1, s)))
    raises(ValueError, lambda: Feedback(tf2, tf4*tf5))
    raises(ValueError, lambda: Feedback(tf2, tf1, 1.5))  # `sign` can only be -1 or 1
    raises(ValueError, lambda: Feedback(tf1, -tf1**-1))  # denominator can't be zero
    raises(ValueError, lambda: Feedback(tf4, tf5))  # Both systems should use the same `var`

