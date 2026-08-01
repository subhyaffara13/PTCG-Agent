
def test_dual(capsys):
    m.captured_dual("a", "b")
    stdout, stderr = capsys.readouterr()
    assert stdout == "a"
    assert stderr == "b"


def test_dual():
    B_x, B_y, B_z, E_x, E_y, E_z = symbols(
        'B_x B_y B_z E_x E_y E_z', real=True)
    F = Matrix((
        (   0,  E_x,  E_y,  E_z),
        (-E_x,    0,  B_z, -B_y),
        (-E_y, -B_z,    0,  B_x),
        (-E_z,  B_y, -B_x,    0)
    ))
    Fd = Matrix((
        (  0, -B_x, -B_y, -B_z),
        (B_x,    0,  E_z, -E_y),
        (B_y, -E_z,    0,  E_x),
        (B_z,  E_y, -E_x,    0)
    ))
    assert F.dual().equals(Fd)
    assert eye(3).dual().equals(zeros(3))
    assert F.dual().dual().equals(-F)


def test_dual():
    B_x, B_y, B_z, E_x, E_y, E_z = symbols(
        'B_x B_y B_z E_x E_y E_z', real=True)
    F = Matrix((
        (   0,  E_x,  E_y,  E_z),
        (-E_x,    0,  B_z, -B_y),
        (-E_y, -B_z,    0,  B_x),
        (-E_z,  B_y, -B_x,    0)
    ))
    Fd = Matrix((
        (  0, -B_x, -B_y, -B_z),
        (B_x,    0,  E_z, -E_y),
        (B_y, -E_z,    0,  E_x),
        (B_z,  E_y, -E_x,    0)
    ))
    assert F.dual().equals(Fd)
    assert eye(3).dual().equals(zeros(3))
    assert F.dual().dual().equals(-F)

