
def test_vector_custom():
    v_a = m.VectorEl()
    v_a.append(m.El(1))
    v_a.append(m.El(2))
    assert str(v_a) == "VectorEl[El{1}, El{2}]"

    vv_a = m.VectorVectorEl()
    vv_a.append(v_a)
    vv_b = vv_a[0]
    assert str(vv_b) == "VectorEl[El{1}, El{2}]"

