
def test_products():
    assert TensorProduct(
        R2.dx, R2.dy)(R2.e_x, R2.e_y) == R2.dx(R2.e_x)*R2.dy(R2.e_y) == 1
    assert TensorProduct(R2.dx, R2.dy)(None, R2.e_y) == R2.dx
    assert TensorProduct(R2.dx, R2.dy)(R2.e_x, None) == R2.dy
    assert TensorProduct(R2.dx, R2.dy)(R2.e_x) == R2.dy
    assert TensorProduct(R2.x, R2.dx) == R2.x*R2.dx
    assert TensorProduct(
        R2.e_x, R2.e_y)(R2.x, R2.y) == R2.e_x(R2.x) * R2.e_y(R2.y) == 1
    assert TensorProduct(R2.e_x, R2.e_y)(None, R2.y) == R2.e_x
    assert TensorProduct(R2.e_x, R2.e_y)(R2.x, None) == R2.e_y
    assert TensorProduct(R2.e_x, R2.e_y)(R2.x) == R2.e_y
    assert TensorProduct(R2.x, R2.e_x) == R2.x * R2.e_x
    assert TensorProduct(
        R2.dx, R2.e_y)(R2.e_x, R2.y) == R2.dx(R2.e_x) * R2.e_y(R2.y) == 1
    assert TensorProduct(R2.dx, R2.e_y)(None, R2.y) == R2.dx
    assert TensorProduct(R2.dx, R2.e_y)(R2.e_x, None) == R2.e_y
    assert TensorProduct(R2.dx, R2.e_y)(R2.e_x) == R2.e_y
    assert TensorProduct(R2.x, R2.e_x) == R2.x * R2.e_x
    assert TensorProduct(
        R2.e_x, R2.dy)(R2.x, R2.e_y) == R2.e_x(R2.x) * R2.dy(R2.e_y) == 1
    assert TensorProduct(R2.e_x, R2.dy)(None, R2.e_y) == R2.e_x
    assert TensorProduct(R2.e_x, R2.dy)(R2.x, None) == R2.dy
    assert TensorProduct(R2.e_x, R2.dy)(R2.x) == R2.dy
    assert TensorProduct(R2.e_y,R2.e_x)(R2.x**2 + R2.y**2,R2.x**2 + R2.y**2) == 4*R2.x*R2.y

    assert WedgeProduct(R2.dx, R2.dy)(R2.e_x, R2.e_y) == 1
    assert WedgeProduct(R2.e_x, R2.e_y)(R2.x, R2.y) == 1

