from typing import Tuple

def test_TensorSymmetry():
    assert TensorSymmetry.fully_symmetric(2) == \
        TensorSymmetry(get_symmetric_group_sgs(2))
    assert TensorSymmetry.fully_symmetric(-3) == \
        TensorSymmetry(get_symmetric_group_sgs(3, True))
    assert TensorSymmetry.direct_product(-4) == \
        TensorSymmetry.fully_symmetric(-4)
    assert TensorSymmetry.fully_symmetric(-1) == \
        TensorSymmetry.fully_symmetric(1)
    assert TensorSymmetry.direct_product(1, -1, 1) == \
        TensorSymmetry.no_symmetry(3)
    assert TensorSymmetry(get_symmetric_group_sgs(2)) == \
        TensorSymmetry(*get_symmetric_group_sgs(2))
    # TODO: add check for *get_symmetric_group_sgs(0)
    sym = TensorSymmetry.fully_symmetric(-3)
    assert sym.rank == 3
    assert sym.base == Tuple(0, 1)
    assert sym.generators == Tuple(Permutation(0, 1)(3, 4), Permutation(1, 2)(3, 4))

