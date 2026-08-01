
def test_latex_vector_expressions():
    A = CoordSys3D('A')

    assert latex(Cross(A.i, A.j*A.x*3+A.k)) == \
        r"\mathbf{\hat{i}_{A}} \times \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}} + \mathbf{\hat{k}_{A}}\right)"
    assert latex(Cross(A.i, A.j)) == \
        r"\mathbf{\hat{i}_{A}} \times \mathbf{\hat{j}_{A}}"
    assert latex(x*Cross(A.i, A.j)) == \
        r"x \left(\mathbf{\hat{i}_{A}} \times \mathbf{\hat{j}_{A}}\right)"
    assert latex(Cross(x*A.i, A.j)) == \
        r'- \mathbf{\hat{j}_{A}} \times \left(\left(x\right)\mathbf{\hat{i}_{A}}\right)'

    assert latex(Curl(3*A.x*A.j)) == \
        r"\nabla\times \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)"
    assert latex(Curl(3*A.x*A.j+A.i)) == \
        r"\nabla\times \left(\mathbf{\hat{i}_{A}} + \left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)"
    assert latex(Curl(3*x*A.x*A.j)) == \
        r"\nabla\times \left(\left(3 \mathbf{{x}_{A}} x\right)\mathbf{\hat{j}_{A}}\right)"
    assert latex(x*Curl(3*A.x*A.j)) == \
        r"x \left(\nabla\times \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)\right)"

    assert latex(Divergence(3*A.x*A.j+A.i)) == \
        r"\nabla\cdot \left(\mathbf{\hat{i}_{A}} + \left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)"
    assert latex(Divergence(3*A.x*A.j)) == \
        r"\nabla\cdot \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)"
    assert latex(x*Divergence(3*A.x*A.j)) == \
        r"x \left(\nabla\cdot \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}}\right)\right)"

    assert latex(Dot(A.i, A.j*A.x*3+A.k)) == \
        r"\mathbf{\hat{i}_{A}} \cdot \left(\left(3 \mathbf{{x}_{A}}\right)\mathbf{\hat{j}_{A}} + \mathbf{\hat{k}_{A}}\right)"
    assert latex(Dot(A.i, A.j)) == \
        r"\mathbf{\hat{i}_{A}} \cdot \mathbf{\hat{j}_{A}}"
    assert latex(Dot(x*A.i, A.j)) == \
        r"\mathbf{\hat{j}_{A}} \cdot \left(\left(x\right)\mathbf{\hat{i}_{A}}\right)"
    assert latex(x*Dot(A.i, A.j)) == \
        r"x \left(\mathbf{\hat{i}_{A}} \cdot \mathbf{\hat{j}_{A}}\right)"

    assert latex(Gradient(A.x)) == r"\nabla \mathbf{{x}_{A}}"
    assert latex(Gradient(A.x + 3*A.y)) == \
        r"\nabla \left(\mathbf{{x}_{A}} + 3 \mathbf{{y}_{A}}\right)"
    assert latex(x*Gradient(A.x)) == r"x \left(\nabla \mathbf{{x}_{A}}\right)"
    assert latex(Gradient(x*A.x)) == r"\nabla \left(\mathbf{{x}_{A}} x\right)"

    assert latex(Laplacian(A.x)) == r"\Delta \mathbf{{x}_{A}}"
    assert latex(Laplacian(A.x + 3*A.y)) == \
        r"\Delta \left(\mathbf{{x}_{A}} + 3 \mathbf{{y}_{A}}\right)"
    assert latex(x*Laplacian(A.x)) == r"x \left(\Delta \mathbf{{x}_{A}}\right)"
    assert latex(Laplacian(x*A.x)) == r"\Delta \left(\mathbf{{x}_{A}} x\right)"

