
def test_mi_dynamic_attributes():
    """Mixing bases with and without dynamic attribute support"""

    for d in (m.VanillaDictMix1(), m.VanillaDictMix2()):
        d.dynamic = 1
        assert d.dynamic == 1

